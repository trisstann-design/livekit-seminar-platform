import asyncio
import logging
from typing import Annotated

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, deepgram, cartesia

logger = logging.getLogger("seminar-agent")


class SeminarAgent:
    """Αυτοματοποιημένος agent για διαχείριση σεμιναρίων"""
    
    def __init__(self):
        self.participants = {}
        self.current_session = None
        self.is_presenting = False
        
    async def entrypoint(self, ctx: JobContext):
        """Entry point για τον agent όταν μπαίνει σε δωμάτιο"""
        
        logger.info(f"🎯 Seminar Agent joining room: {ctx.room.name}")
        
        # Συνδέουμε τον agent στο δωμάτιο
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        
        # Ρύθμιση του voice assistant
        assistant = VoiceAssistant(
            vad=deepgram.VAD.load(),
            stt=deepgram.STT(),
            llm=openai.LLM(
                model="gpt-4o-mini",
                instructions="""Είσαι ο host ενός σεμιναρίου. 
                Καλωσόρισε τους συμμετέχοντες, 
                διαχειρίσου τις ερωτήσεις, και 
                κράτα το σεμινάριο οργανωμένο.
                Μίλα στα ελληνικά.""",
            ),
            tts=cartesia.TTS(),
            chat_ctx=llm.ChatContext(),
        )
        
        # Ενεργοποίηση του assistant
        assistant.start(ctx.room)
        
        # Παρακολούθηση events
        await self._setup_event_handlers(ctx)
        
        # Καλωσόρισμα
        await self._welcome_message(assistant)
        
        # Αναμονή μέχρι το τέλος της συνεδρίας
        await assistant.aclose()
        
    async def _setup_event_handlers(self, ctx: JobContext):
        """Ρύθμιση event handlers για το δωμάτιο"""
        
        @ctx.room.on("participant_connected")
        def on_participant_connected(participant: rtc.RemoteParticipant):
            logger.info(f"👤 Participant joined: {participant.identity}")
            
        @ctx.room.on("participant_disconnected")
        def on_participant_disconnected(participant: rtc.RemoteParticipant):
            logger.info(f"👋 Participant left: {participant.identity}")
            
        @ctx.room.on("data_received")
        def on_data_received(data: rtc.DataPacket):
            logger.info(f"📨 Data received: {data.data.decode()}")
            
    async def _welcome_message(self, assistant):
        """Μήνυμα καλωσορίσματος"""
        welcome_text = "Καλώς ήρθατε στο σεμινάριό μας! Είμαι ο AI assistant που θα σας βοηθήσει."
        await assistant.say(welcome_text)


def main():
    """Main function για εκκίνηση του agent"""
    
    # Ρύθμιση logging
    logging.basicConfig(level=logging.INFO)
    
    # Δημιουργία agent instance
    agent = SeminarAgent()
    
    # CLI εκκίνηση
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=agent.entrypoint,
            # Ρυθμίσεις για auto-join σε δωμάτια
            prewarm_fnc=lambda: logger.info("🚀 Agent prewarming..."),
        )
    )


if __name__ == "__main__":
    main()