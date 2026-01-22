import React, { useState, useEffect, useRef } from 'react';
import CameraView from './components/CameraView';
import AudioRecorder from './components/AudioRecorder';
import ChatInterface from './components/ChatInterface';
import EnrollmentForm from './components/EnrollmentForm';
import AvatarCanvas from './components/AvatarCanvas';
import axios from 'axios';
import { Maximize2, Minimize2 } from 'lucide-react';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import CaregiverDashboard from './pages/CaregiverDashboard';
import NavBar from './components/SideNav'; // Imported as NavBar

const API_BASE = "http://localhost:8000/api/v1";


function App() {
  const [view, setView] = useState('landing');
  const [mode, setMode] = useState('person');
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hello! Show me a face or object, or ask me a question." }
  ]);
  const [suggestions, setSuggestions] = useState([]);
  const [currentPerson, setCurrentPerson] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [avatarMessage, setAvatarMessage] = useState(null);
  const [isCameraExpanded, setIsCameraExpanded] = useState(true); // Default Expanded
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState(""); // Granular Status

  const [enrollType, setEnrollType] = useState('person'); // 'person' or 'object'

  // UseRef to trigger camera capture from outside
  const cameraTriggerRef = useRef(null);

  const [captureTrigger, setCaptureTrigger] = useState(0);
  const [enrollData, setEnrollData] = useState(null);

  // Handlers
  const triggerScanFace = () => {
    setMode('person');
    setCaptureTrigger(Date.now());
  };

  const triggerScanObject = () => {
    setMode('object');
    setCaptureTrigger(Date.now());
  };

  const handleEnrollSave = async (data) => {
    setEnrollData({ ...data, type: enrollType });
    setMode('enroll_capture');
    setCaptureTrigger(Date.now());
  };

  useEffect(() => {
    setSuggestions([
      "Who is this?",
      "Where is my wallet?",
      "Enroll new person",
      "Enroll new object"
    ]);
  }, []);

  const handleSuggestionClick = (text) => {
    if (text === "Enroll new person") {
      setEnrollType('person');
      setMode('enroll_ui');
    } else if (text === "Enroll new object") {
      setEnrollType('object');
      setMode('enroll_ui');
    } else {
      handleSendMessage(text);
    }
  };

  const handleCapture = async (blob) => {
    setIsProcessing(true);
    const formData = new FormData();

    if (mode === 'enroll_capture' && enrollData) {
      formData.append('file', blob, 'enroll.jpg');
      formData.append('name', enrollData.name);
      formData.append('notes', enrollData.notes);

      try {
        if (enrollData.type === 'object') {
          await axios.post(`${API_BASE}/remember/object`, formData);
          addBotMessage(`I've remembered your ${enrollData.name}.`);
          speakResponse(`I have remembered your ${enrollData.name}.`);
        } else {
          formData.append('relation', enrollData.relation);
          if (enrollData.age) formData.append('age', enrollData.age);
          if (enrollData.audioBlob) {
            formData.append('audio_file', enrollData.audioBlob, 'voice.webm');
          }
          const res = await axios.post(`${API_BASE}/remember/person`, formData);
          if (res.data.avatar_url) {
            addBotMessage(`I've remembered ${enrollData.name}. (Avatar Created)`);
          } else {
            addBotMessage(`I've remembered ${enrollData.name}.`);
          }
          speakResponse(`I have remembered ${enrollData.name}.`);
        }
        setMode('person');
        setEnrollData(null);
      } catch (e) {
        console.error(e);
        addBotMessage("Failed to enroll.");
      } finally {
        setIsProcessing(false);
      }
      return;
    }

    formData.append('file', blob, 'capture.jpg');

    try {
      let endpoint = mode === 'person' ? `${API_BASE}/recognize/person` : `${API_BASE}/find/object`;
      const res = await axios.post(endpoint, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      const data = res.data;

      if (mode === 'person' && data.status === 'identified') {
        setCurrentPerson(data.person);
        addBotMessage(`I see ${data.person.name}.`);
        updateSuggestions(data.person);
        speakResponse(`Hello ${data.person.name}.`);
      } else if (mode === 'object' && data.status === 'identified') {
        const loc = data.object.location || "unknown location";
        addBotMessage(`I found your ${data.object.name}. It is usually in ${loc}.`);
        speakResponse(`That is your ${data.object.name}. Location: ${loc}.`);
      } else if (mode === 'object' && data.status === 'generic_detection') {
        const objects = data.objects.map(o => o.object).join(", ");
        addBotMessage(`I see: ${objects}. (Not in my personal memory)`);
        speakResponse(`I see ${objects}.`);
      } else {
        addBotMessage(`I don't recognize that ${mode}.`);
        speakResponse(`I don't know who that is.`);
        // Optional: Trigger enrollment suggestion?
      }
    } catch (err) {
      console.error(err);
      addBotMessage("Error processing image.");
    } finally {
      setIsProcessing(false);
    }
  };

  const updateSuggestions = (person) => {
    setSuggestions([
      `Who is ${person.name}?`,
      `How does ${person.name} talk?`,
      `Any notes on ${person.name}?`
    ]);
  };

  const handleSendMessage = async (text) => {
    setIsProcessing(true);
    setProcessingStatus("Accessing Memory Bank...");

    // Simulate steps for better UX
    const statusInterval = setInterval(() => {
      setProcessingStatus(prev => {
        if (prev === "Accessing Memory Bank...") return "Consulting LLM Cortex...";
        if (prev === "Consulting LLM Cortex...") return "Synthesizing Response...";
        return prev;
      });
    }, 1500);

    setMessages(prev => [...prev, { role: 'user', text }]);
    let responseText = "I'm not sure about that.";
    let audioUrl = null;
    let imageBase64 = null;

    try {
      if (currentPerson && (text.toLowerCase().includes("talk") || text.toLowerCase().includes("voice"))) {
        // ... existing voice logic ...
        if (currentPerson.audio) {
          responseText = `Here is the voice of ${currentPerson.name}.`;
          try {
            const binaryString = window.atob(currentPerson.audio);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
            }
            const blob = new Blob([bytes], { type: 'audio/webm' });
            audioUrl = URL.createObjectURL(blob);
          } catch (e) {
            responseText = "I found a voice record but couldn't play it.";
          }
        } else {
          responseText = `I don't have a voice sample for ${currentPerson.name}.`;
        }

        clearInterval(statusInterval);
        setProcessingStatus("Retrieving Voice Sample...");

        setTimeout(() => {
          addBotMessage(responseText, audioUrl);
          speakResponse(responseText);
          setIsProcessing(false);
          setProcessingStatus("");
        }, 800);
        return;
      }

      const res = await axios.post(`${API_BASE}/chat/query`, { text });

      clearInterval(statusInterval);
      setProcessingStatus("Finalizing...");

      const data = res.data;
      if (data.status === 'found') {
        responseText = data.text;
        if (data.audio_base64) {
          try {
            const binaryString = window.atob(data.audio_base64);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
            }
            const blob = new Blob([bytes], { type: 'audio/webm' });
            audioUrl = URL.createObjectURL(blob);
          } catch (e) { }
        }
        if (data.image_base64) imageBase64 = data.image_base64;
        if (data.person) {
          setCurrentPerson(data.person);
          updateSuggestions(data.person);
        }
      } else {
        responseText = data.text || "I don't know who that is.";
      }
      addBotMessage(responseText, audioUrl, imageBase64, data.gallery);
      speakResponse(responseText);
    } catch (e) {
      clearInterval(statusInterval);
      console.error(e);
      responseText = "I had trouble searching my memory.";
      addBotMessage(responseText);
      speakResponse(responseText);
    } finally {
      if (!((currentPerson && (text.toLowerCase().includes("talk") || text.toLowerCase().includes("voice"))))) {
        setIsProcessing(false);
        setProcessingStatus("");
      }
    }
  };

  const addBotMessage = (text, audioUrl = null, imageBase64 = null, gallery = []) => {
    setMessages(prev => [...prev, { role: 'bot', text, audioUrl, image: imageBase64, gallery }]);
  };

  const speakResponse = (text) => {
    setIsSpeaking(true);
    setAvatarMessage(text);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onend = () => {
      setIsSpeaking(false);
      setAvatarMessage(null);
    };
    window.speechSynthesis.speak(utterance);
  };

  // VIEW ROUTING
  let content;
  if (view === 'landing') {
    content = <LandingPage onGetStarted={() => setView('login')} />;
  }
  else if (view === 'login') {
    content = (
      <LoginPage onSelectRole={(role) => {
        if (role === 'caregiver') setView('caregiver');
        else setView('patient');
      }} />
    );
  }
  else if (view === 'caregiver') {
    content = <CaregiverDashboard />;
  } else {
    // Patient App Content
    content = (
      <div className="app-container">
        {/* MAIN STAGE (FULL WIDTH) */}
        <div className="main-stage">
          <div className="avatar-zone">
            <AvatarCanvas isSpeaking={isSpeaking} isProcessing={isProcessing} processingStatus={processingStatus} message={avatarMessage} />
          </div>
          <div className="chat-zone">
            {mode === 'enroll_ui' ? (
              <EnrollmentForm
                type={enrollType}
                onCancel={() => setMode('person')}
                onSave={handleEnrollSave}
              />
            ) : (
              <ChatInterface
                messages={messages}
                onSendMessage={handleSendMessage}
                suggestions={suggestions}
                onSuggestionClick={handleSuggestionClick}
                onPlayAudio={(url) => new Audio(url).play()}
                onCapture={handleCapture}
                onScanFace={() => { setMode('person'); }}
                onScanObject={() => { setMode('object'); }}
                onEnroll={() => { setEnrollType('person'); setMode('enroll_ui'); }}
                onEnrollObject={() => { setEnrollType('object'); setMode('enroll_ui'); }}
                isTyping={isProcessing}
                typingStatus={processingStatus}
                captureTrigger={captureTrigger}
                enrollType={enrollType}
              />
            )}
          </div>
        </div>

        <style>{`
        :root { --bg: #0f172a; --surface: #1e293b; --primary: #8b5cf6; --text: #f8fafc; }
        .app-container {
            display: flex;
            height: 100%; /* CHANGED from 100vh to fit inside NavWrapper */
            background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
            color: var(--text);
            overflow: hidden;
            flex-direction: row; 
            width: 100%;
        }
        .main-stage {
            flex: 1;
            display: flex;
            flex-direction: row; /* Side by side */
            position: relative;
            background: transparent;
            overflow: hidden;
        }
        .avatar-zone {
            width: 500px; /* Increased from 400px */
            height: 100%;
            position: relative;
            background: transparent;
            flex-shrink: 0;
            z-index: 10;
        }
        .chat-zone {
            flex: 1;
            height: 100%;
            padding: 0;
            box-sizing: border-box;
            display: flex;
            justify-content: center;
            overflow: hidden;
            background: transparent;
        }
      `}</style>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: '#0f172a', overflow: 'hidden' }}>
      <NavBar onViewChange={setView} currentView={view} />
      <div style={{ flex: 1, paddingTop: '70px', height: '100%', overflow: 'hidden' }}>
        {content}
      </div>
    </div>
  );
}

export default App;
