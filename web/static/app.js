// Finance Reel Factory - Studio Frontend Controller

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const ollamaBadge = document.getElementById("ollama-badge");
  const modelSelect = document.getElementById("ollama-model-select");
  const btnPullModel = document.getElementById("btn-pull-model");
  const aiPrompt = document.getElementById("ai-prompt");
  const btnGenerateScript = document.getElementById("btn-generate-script");
  const btnRefineScript = document.getElementById("btn-refine-script");
  const scriptContent = document.getElementById("script-content");
  
  const projectIdInput = document.getElementById("project-id");
  const reelTitleInput = document.getElementById("reel-title");
  const voiceSelect = document.getElementById("voice-select");
  const burnSubtitlesCheck = document.getElementById("burn-subtitles");
  
  const btnRenderReel = document.getElementById("btn-render-reel");
  const renderBtnText = document.getElementById("render-btn-text");
  const renderSpinner = document.getElementById("render-spinner");
  const statusConsole = document.getElementById("status-console");
  const statusMessage = document.getElementById("status-message");
  
  const reelPlayer = document.getElementById("reel-player");
  const videoSource = document.getElementById("video-source");
  const videoPlaceholder = document.getElementById("video-placeholder");
  const btnDownloadMp4 = document.getElementById("btn-download-mp4");
  const btnDownloadZip = document.getElementById("btn-download-zip");
  const thumbnailsGrid = document.getElementById("slide-thumbnails-grid");

  // 1. Check System Status & Ollama Models
  async function checkSystem() {
    try {
      const res = await fetch("/api/system/status");
      const data = await res.json();
      if (data.ollama_connected) {
        ollamaBadge.textContent = "Ollama: Connected";
        ollamaBadge.className = "badge badge-success";
      } else {
        ollamaBadge.textContent = "Ollama: Offline";
        ollamaBadge.className = "badge badge-warning";
      }
    } catch (e) {
      ollamaBadge.textContent = "Server: Offline";
      ollamaBadge.className = "badge badge-warning";
    }

    // Load models
    try {
      const res = await fetch("/api/ollama/models");
      const data = await res.json();
      if (data.models && data.models.length > 0) {
        modelSelect.innerHTML = "";
        data.models.forEach(m => {
          const opt = document.createElement("option");
          opt.value = m;
          opt.textContent = m;
          modelSelect.appendChild(opt);
        });
      }
    } catch (e) {
      console.warn("Could not list Ollama models:", e);
    }
  }

  // 2. Pull / Download Model via Ollama
  btnPullModel.addEventListener("click", async () => {
    const modelToPull = prompt("Enter Ollama model name to pull (e.g. llama3.2:1b, mistral, qwen2.5:1.5b):", "llama3.2:1b");
    if (!modelToPull) return;
    
    btnPullModel.textContent = "Pulling...";
    btnPullModel.disabled = true;
    showStatus(`Pulling model '${modelToPull}' from Ollama library... This might take a few minutes.`);

    try {
      const res = await fetch("/api/ollama/pull", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: modelToPull })
      });
      const data = await res.json();
      alert(`Model pull finished: ${data.message || 'Done'}`);
      checkSystem();
    } catch (err) {
      alert("Error pulling model: " + err.message);
    } finally {
      btnPullModel.textContent = "Pull";
      btnPullModel.disabled = false;
    }
  });

  // 3. AI Script Generation / Prompt
  async function handleAiScript(instruction) {
    const promptText = aiPrompt.value.trim();
    if (!promptText && instruction === "new") {
      alert("Please write a prompt for the video topic (e.g., 'Compare buying Gold vs Real Estate')");
      aiPrompt.focus();
      return;
    }

    const originalBtn = instruction === "new" ? btnGenerateScript : btnRefineScript;
    const originalText = originalBtn.innerHTML;
    originalBtn.innerHTML = "<span>⏳ Thinking with Ollama...</span>";
    originalBtn.disabled = true;
    showStatus(`Ollama is drafting script with model: ${modelSelect.value}...`);

    try {
      const res = await fetch("/api/ollama/generate_script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: promptText,
          topic: reelTitleInput.value,
          current_script: scriptContent.value,
          model: modelSelect.value,
          instruction: instruction
        })
      });
      const data = await res.json();
      if (data.success && data.script) {
        scriptContent.value = data.script.trim();
        showStatus("✨ Script generated successfully! You can edit it or click Render Reel.");
      } else {
        alert("Ollama Error: " + (data.error || "Failed to generate script."));
      }
    } catch (err) {
      alert("Error contacting Ollama assistant: " + err.message);
    } finally {
      originalBtn.innerHTML = originalText;
      originalBtn.disabled = false;
    }
  }

  btnGenerateScript.addEventListener("click", () => handleAiScript("new"));
  btnRefineScript.addEventListener("click", () => handleAiScript("refine"));

  // 4. Render Full Reel
  btnRenderReel.addEventListener("click", async () => {
    const projectId = projectIdInput.value.trim() || "REEL_001_SIP_FD_REALITY_CHECK";
    const title = reelTitleInput.value.trim() || "SIP & FD Reality Check";
    const script = scriptContent.value.trim();
    const voice = voiceSelect.value;
    const burnSubtitles = burnSubtitlesCheck.checked;

    if (!script) {
      alert("Please provide a voiceover script.");
      return;
    }

    // UI Loading state
    btnRenderReel.disabled = true;
    renderBtnText.textContent = "Rendering Reel (Slides + Neural TTS + Subtitles)...";
    renderSpinner.classList.remove("hidden");
    showStatus("Step 1/3: Drawing high-res slides with modular templates...");

    try {
      const res = await fetch("/api/render", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: projectId,
          title: title,
          script_text: script,
          voice: voice,
          burn_subtitles: burnSubtitles
        })
      });

      const data = await res.json();
      if (data.success) {
        showStatus("🎉 Reel assembled and burned-in subtitles completed successfully!");
        
        // Update Video Player with cache-busting timestamp
        const t = new Date().getTime();
        const videoUrl = `${data.video_url}?t=${t}`;
        videoSource.src = videoUrl;
        reelPlayer.load();
        videoPlaceholder.classList.add("hidden");
        
        // Update Download links
        btnDownloadMp4.href = videoUrl;
        btnDownloadMp4.download = `${projectId}_final.mp4`;
        btnDownloadZip.href = `/api/download/${projectId}?t=${t}`;
        
        // Refresh Slide Thumbnails
        loadThumbnails(projectId);

        // Auto-play preview
        setTimeout(() => {
          reelPlayer.play().catch(() => {});
        }, 500);
      } else {
        alert("Render Error: " + (data.detail || "Unknown error"));
      }
    } catch (err) {
      alert("Pipeline Error: " + err.message);
    } finally {
      btnRenderReel.disabled = false;
      renderBtnText.textContent = "🎬 Generate & Render Full Reel";
      renderSpinner.classList.add("hidden");
    }
  });

  // 5. Load Slide Thumbnails
  async function loadThumbnails(projectId) {
    try {
      const res = await fetch(`/api/slides/${projectId}`);
      const data = await res.json();
      thumbnailsGrid.innerHTML = "";
      if (data.slides && data.slides.length > 0) {
        data.slides.forEach((url, i) => {
          const div = document.createElement("div");
          div.className = "slide-thumb";
          div.title = `Slide ${i+1}`;
          div.innerHTML = `<img src="${url}" alt="Slide ${i+1}">`;
          div.onclick = () => window.open(url, "_blank");
          thumbnailsGrid.appendChild(div);
        });
      }
    } catch (e) {
      console.warn("Could not load thumbnails:", e);
    }
  }

  function showStatus(msg) {
    statusConsole.classList.remove("hidden");
    statusMessage.textContent = msg;
  }

  // Initialize on load
  checkSystem();
  loadThumbnails(projectIdInput.value);
});
