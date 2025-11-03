# 🎯 LiveKit Seminar Platform

**Αυτοματοποιημένη πλατφόρμα σεμιναρίων με AI Agents**

## 📋 Περιγραφή

Η **LiveKit Seminar Platform** είναι μια ολοκληρωμένη λύση που συνδυάζει:
- **Video Conferencing** με το LiveKit Meet
- **AI-powered Agents** για αυτόματη διαχείριση σεμιναρίων  
- **Αυτόματη ανάθεση** agents σε νέα δωμάτια
- **Ελληνικά UI/UX** και φωνητικές αλληλεπιδράσεις

## 🏗️ Αρχιτεκτονική

```
LiveKit-Seminar-Platform/
├── 🎥 frontend/          (Next.js Meet Interface)
├── 🤖 agent/            (Python AI Agent)
├── 🔧 server/           (Room Orchestrator)
└── 📊 analytics/        (Logs & Metrics)
```

## ⚡ Βασικά Χαρακτηριστικά

### 🤖 **Αυτόματος AI Agent**
- **Αυτόματη είσοδος** σε νέα δωμάτια σεμιναρίων
- **Ελληνικό interface** και φωνητικές αλληλεπιδράσεις
- **Καλωσόρισμα συμμετεχόντων**
- **Διαχείριση ερωτήσεων** και chat
- **Οργάνωση παρουσιάσεων**

### 🏠 **Room Orchestrator**
- **Δημιουργία δωματίων** σεμιναρίων
- **Αυτόματη ανάπτυξη** agents
- **Παρακολούθηση κατάστασης** δωματίων
- **Cleanup και διαχείριση resources**

### 🎥 **Frontend Integration** 
- **Προσαρμοσμένο Meet UI**
- **Integration με LiveKit Cloud**
- **Real-time chat και video**

## 🚀 Γρήγορη Εκκίνηση

### 1. **Setup Environment**

```bash
# Clone το repository
git clone https://github.com/trisstann-design/livekit-seminar-platform.git
cd livekit-seminar-platform

# Setup environment variables
cp .env.example .env.local
```

### 2. **Ρύθμιση LiveKit Credentials**

```bash
# Στο .env.local file:
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
```

### 3. **Εκκίνηση Agent**

```bash
# Εγκατάσταση dependencies
cd agent/
pip install -r requirements.txt

# Εκκίνηση agent
python seminar_agent.py dev
```

### 4. **Εκκίνηση Room Orchestrator**

```bash
# Σε νέο terminal
cd server/
python room_orchestrator.py
```

### 5. **Frontend Setup**

```bash
# Clone του forked meet repo
git clone https://github.com/trisstann-design/meet.git frontend/
cd frontend/

# Εγκατάσταση και εκκίνηση
pnpm install
pnpm dev
```

## 🔧 Χρήση της Πλατφόρμας

### **Δημιουργία Σεμιναρίου**

```python
from server.room_orchestrator import RoomOrchestrator

# Δημιουργία orchestrator
orchestrator = RoomOrchestrator()

# Δημιουργία νέου σεμιναρίου
room_name = await orchestrator.create_seminar_room(
    seminar_id="ai-intro-2024",
    seminar_title="Εισαγωγή στην Τεχνητή Νοημοσύνη",
    max_participants=50
)

print(f"✅ Σεμινάριο δημιουργήθηκε: {room_name}")
```

### **Αυτόματη Ανάθεση Agent**

Όταν δημιουργείται ένα νέο δωμάτιο:

1. 🏠 **Room Orchestrator** δημιουργεί το δωμάτιο
2. 🤖 **Agent** αναπτύσσεται αυτόματα
3. 👋 **Καλωσόρισμα** συμμετεχόντων
4. 🎤 **Διαχείριση** παρουσίασης

### **Agent Capabilities**

```python
# Ο Agent μπορεί να:
- καλωσορίσει συμμετέχοντες
- απαντήσει σε ερωτήσεις
- διαχειριστεί το chat
- οργανώσει παρουσιάσεις
- καταγράψει metrics
```

## 📊 Monitoring & Analytics

### **Room Status**
```python
# Έλεγχος κατάστασης
status = orchestrator.get_room_status("seminar-ai-intro-2024")
print(f"Participants: {len(status['participants'])}")
print(f"Agent Active: {status['agent_deployed']}")
```

### **Active Rooms**
```python
# Λίστα ενεργών δωματίων
active_rooms = orchestrator.list_active_rooms()
for room in active_rooms:
    print(f"🏠 {room}")
```

## 🔗 Integration με Existing Systems

### **VAPI Integration**
```python
# Στον agent μπορείτε να προσθέσετε:
from vapi import VAPIClient

class SeminarAgent:
    def __init__(self):
        self.vapi_client = VAPIClient()
    
    async def handle_telephony_call(self, call_data):
        # Handle VAPI calls στο σεμινάριο
        pass
```

### **Google Sheets Logging**
```python
# Καταγραφή σε Google Sheets
from gspread import service_account

class SeminarAgent:
    async def log_participant_data(self, participant_info):
        # Log στο Google Sheet σας
        sheet = self.gc.open("Seminar-Logs").sheet1
        sheet.append_row([participant_info])
```

## 🎯 Επόμενα Βήματα

1. **✅ Fork repositories** (COMPLETED)
2. **✅ Create main project structure** (COMPLETED)
3. **🔧 Setup local development**
4. **🤖 Customize agent behavior**
5. **🎨 Customize frontend UI**  
6. **🚀 Deploy to production**

## 🆘 Support & Documentation

- **LiveKit Docs**: https://docs.livekit.io/
- **LiveKit Agents Guide**: https://docs.livekit.io/agents/
- **Repository Issues**: [Create Issue](https://github.com/trisstann-design/livekit-seminar-platform/issues)

---

**Δημιουργήθηκε από [trisstann-design](https://github.com/trisstann-design) για αυτοματοποιημένα σεμινάρια με AI** 🚀