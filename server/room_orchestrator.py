import asyncio
import logging
from typing import Dict, List, Optional
from livekit import api, rtc
from livekit.api import Room, CreateRoomRequest
import os

logger = logging.getLogger("room-orchestrator")


class RoomOrchestrator:
    """Διαχειριστής δωματίων και agents"""
    
    def __init__(self):
        self.livekit_api = api.LiveKitAPI(
            url=os.getenv('LIVEKIT_URL'),
            api_key=os.getenv('LIVEKIT_API_KEY'),
            api_secret=os.getenv('LIVEKIT_API_SECRET')
        )
        self.active_rooms: Dict[str, Dict] = {}
        self.agent_processes: Dict[str, asyncio.subprocess.Process] = {}
    
    async def create_seminar_room(self, 
                                  seminar_id: str, 
                                  seminar_title: str,
                                  max_participants: int = 100,
                                  enable_recording: bool = True) -> str:
        """Δημιουργία δωματίου για σεμινάριο"""
        
        room_name = f"seminar-{seminar_id}"
        
        try:
            # Δημιουργία δωματίου
            room_request = CreateRoomRequest(
                name=room_name,
                max_participants=max_participants,
                metadata=f'{{"title": "{seminar_title}", "type": "seminar"}}'
            )
            
            room = await self.livekit_api.room.create_room(room_request)
            
            # Αποθήκευση πληροφοριών
            self.active_rooms[room_name] = {
                'seminar_id': seminar_id,
                'title': seminar_title,
                'room': room,
                'participants': {},
                'agent_deployed': False,
                'created_at': asyncio.get_event_loop().time()
            }
            
            logger.info(f"🏠 Created room: {room_name} for seminar: {seminar_title}")
            
            # Αυτόματη ανάπτυξη agent
            await self.deploy_agent_to_room(room_name)
            
            return room_name
            
        except Exception as e:
            logger.error(f"❌ Error creating room {room_name}: {str(e)}")
            raise
    
    async def deploy_agent_to_room(self, room_name: str) -> bool:
        """Ανάπτυξη agent σε συγκεκριμένο δωμάτιο"""
        
        if room_name not in self.active_rooms:
            logger.error(f"❌ Room {room_name} not found")
            return False
        
        try:
            # Εκκίνηση agent process
            cmd = [
                'python', 
                'agent/seminar_agent.py',
                'start',
                '--room', room_name
            ]
            
            env = os.environ.copy()
            env.update({
                'LIVEKIT_URL': os.getenv('LIVEKIT_URL'),
                'LIVEKIT_API_KEY': os.getenv('LIVEKIT_API_KEY'),
                'LIVEKIT_API_SECRET': os.getenv('LIVEKIT_API_SECRET')
            })
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.agent_processes[room_name] = process
            self.active_rooms[room_name]['agent_deployed'] = True
            
            logger.info(f"🤖 Agent deployed to room: {room_name}")
            
            # Παρακολούθηση του process
            asyncio.create_task(self._monitor_agent_process(room_name, process))
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error deploying agent to {room_name}: {str(e)}")
            return False
    
    async def _monitor_agent_process(self, room_name: str, process: asyncio.subprocess.Process):
        """Παρακολούθηση agent process"""
        
        try:
            return_code = await process.wait()
            logger.info(f"🔍 Agent process for {room_name} exited with code: {return_code}")
            
            # Καθαρισμός
            if room_name in self.agent_processes:
                del self.agent_processes[room_name]
                
            if room_name in self.active_rooms:
                self.active_rooms[room_name]['agent_deployed'] = False
                
        except Exception as e:
            logger.error(f"❌ Error monitoring agent for {room_name}: {str(e)}")
    
    async def stop_agent_in_room(self, room_name: str) -> bool:
        """Τερματισμός agent σε συγκεκριμένο δωμάτιο"""
        
        if room_name not in self.agent_processes:
            logger.warning(f"⚠️ No agent process found for room: {room_name}")
            return False
        
        try:
            process = self.agent_processes[room_name]
            process.terminate()
            
            # Αναμονή termination
            try:
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                # Force kill αν δεν terminate gracefully
                process.kill()
                await process.wait()
            
            # Cleanup
            del self.agent_processes[room_name]
            if room_name in self.active_rooms:
                self.active_rooms[room_name]['agent_deployed'] = False
            
            logger.info(f"✅ Agent stopped in room: {room_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error stopping agent in {room_name}: {str(e)}")
            return False
    
    async def close_seminar_room(self, room_name: str) -> bool:
        """Κλείσιμο δωματίου και καθαρισμός"""
        
        try:
            # Τερματισμός agent
            await self.stop_agent_in_room(room_name)
            
            # Κλείσιμο δωματίου
            await self.livekit_api.room.delete_room(
                api.DeleteRoomRequest(room=room_name)
            )
            
            # Cleanup
            if room_name in self.active_rooms:
                del self.active_rooms[room_name]
            
            logger.info(f"🗑️ Room closed: {room_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error closing room {room_name}: {str(e)}")
            return False
    
    def get_room_status(self, room_name: str) -> Optional[Dict]:
        """Λήψη κατάστασης δωματίου"""
        return self.active_rooms.get(room_name)
    
    def list_active_rooms(self) -> List[str]:
        """Λίστα ενεργών δωματίων"""
        return list(self.active_rooms.keys())


# Παράδειγμα χρήσης
async def main():
    """Παράδειγμα δημιουργίας σεμιναρίου"""
    
    orchestrator = RoomOrchestrator()
    
    # Δημιουργία σεμιναρίου
    room_name = await orchestrator.create_seminar_room(
        seminar_id="test-001",
        seminar_title="Περί LiveKit Agents"
    )
    
    print(f"✅ Seminar room created: {room_name}")
    print(f"🔗 Join URL: https://meet.livekit.io/custom?liveKitUrl={os.getenv('LIVEKIT_URL')}&token=<PARTICIPANT_TOKEN>")
    
    # Αναμονή...
    await asyncio.sleep(30)
    
    # Κλείσιμο
    await orchestrator.close_seminar_room(room_name)


if __name__ == "__main__":
    asyncio.run(main())