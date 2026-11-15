// Finance Reel Factory - Studio Frontend Controller

document.addEventListener("DOMContentLoaded", () => {
  // Core UI Elements
  const ollamaBadge = document.getElementById("ollama-badge");
  const modelSelect = document.getElementById("ollama-model-select");
  const btnPullModel = document.getElementById("btn-pull-model");
  const aiPrompt = document.getElementById("ai-prompt");
  const btnGenerateScript = document.getElementById("btn-generate-script");
  const btnRefineScript = document.getElementById("btn-refine-script");
  const scriptContent = document.getElementById("script-content");
  
  const projectIdInput = document.getElementById("project-id");
  const reelTitleInput = document.getElementById("reel-title");
  
  // Cat Memes Elements
  const catTemplatesBar = document.getElementById("cat-templates-bar");
  const btnSearchCatsModal = document.getElementById("btn-search-cats-modal");
  const internetCatDrawer = document.getElementById("internet-cat-drawer");
  const internetCatQuery = document.getElementById("internet-cat-query");
  const btnDoCatSearch = document.getElementById("btn-do-cat-search");
  const internetCatResults = document.getElementById("internet-cat-results");
  let selectedCatTemplate = "viral_cats";

  // Voice & Caption Elements
  const voiceSelect = document.getElementById("voice-select");
  const voiceStyleSelect = document.getElementById("voice-style-select");
  const captionStyleSelect = document.getElementById("caption-style-select");
  const burnSubtitlesCheck = document.getElementById("burn-subtitles");
  
  // Render & Status Elements
  const btnRenderReel = document.getElementById("btn-render-reel");
  const renderBtnText = document.getElementById("render-btn-text");
  const renderSpinner = document.getElementById("render-spinner");
  const statusConsole = document.getElementById("status-console");
  const statusMessage = document.getElementById("status-message");
  
  // Preview & Download Elements
  const reelPlayer = document.getElementById("reel-player");
  const videoSource = document.getElementById("video-source");
  const videoPlaceholder = document.getElementById("video-placeholder");
  const btnDownloadMp4 = document.getElementById("btn-download-mp4");
  const btnDownloadPptx = document.getElementById("btn-download-pptx");
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
          if (m === "llama3.2:1b") opt.selected = true;
          modelSelect.appendChild(opt);
        });
      }
    } catch (e) {
      console.warn("Could not list Ollama models:", e);
    }
  }

  // 2. Load Cat Meme Templates
  async function loadCatTemplates() {
    try {
      const res = await fetch("/api/cats/templates");
      const data = await res.json();
      catTemplatesBar.innerHTML = "";
      if (data.cats && data.cats.length > 0) {
        data.cats.forEach((cat, index) => {
          const card = document.createElement("div");
          card.className = "cat-template-card" + (index === 0 ? " active" : "");
          card.innerHTML = `
            <img src="${cat.url}" alt="${cat.name}">
            <span>${cat.name}</span>
          `;
          card.onclick = () => {
            document.querySelectorAll(".cat-template-card").forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            selectedCatTemplate = cat.id;
          };
          catTemplatesBar.appendChild(card);
        });
      }
    } catch (e) {
      console.warn("Error loading cat templates:", e);
    }
  }

  // 3. Internet Cat Search Drawer
  btnSearchCatsModal.addEventListener("click", () => {
    internetCatDrawer.classList.toggle("hidden");
  });

  btnDoCatSearch.addEventListener("click", async () => {
    const q = internetCatQuery.value.trim() || "funny cat meme";
    btnDoCatSearch.textContent = "Searching...";
    btnDoCatSearch.disabled = true;

    try {
      const res = await fetch("/api/cats/fetch_internet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, limit: 6 })
      });
      const data = await res.json();
      internetCatResults.innerHTML = "";
      if (data.results && data.results.length > 0) {
        data.results.forEach(item => {
          const card = document.createElement("div");
          card.className = "internet-cat-card";
          card.innerHTML = `
            <img src="${item.url}" alt="${item.title}">
            <button class="btn btn-secondary btn-sm">Use Meme</button>
          `;
          card.querySelector("button").onclick = async () => {
            card.querySelector("button").textContent = "Grabbing...";
            try {
              const grabRes = await fetch("/api/cats/grab", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ asset_url: item.url, cat_name: item.title })
              });
              const grabData = await grabRes.json();
              alert("Cat Meme added to your library!");
              loadCatTemplates();
            } catch (err) {
              alert("Failed to grab cat: " + err.message);
            }
          };
          internetCatResults.appendChild(card);
        });
      } else {
        internetCatResults.innerHTML = "<p style='grid-column: span 3; font-size: 12px; color: var(--text-muted);'>No results found on Wikimedia Commons. Try another term.</p>";
      }
    } catch (err) {
      alert("Error searching internet cats: " + err.message);
    } finally {
      btnDoCatSearch.textContent = "Search Wikimedia";
      btnDoCatSearch.disabled = false;
    }
  });

  // 4. Pull Model via Ollama
  btnPullModel.addEventListener("click", async () => {
    const modelToPull = prompt("Enter Ollama model name to pull (e.g. llama3.2:1b, qwen2.5:1.5b):", "llama3.2:1b");
    if (!modelToPull) return;
    
    btnPullModel.textContent = "Pulling...";
    btnPullModel.disabled = true;
    showStatus(`Pulling model '${modelToPull}' from Ollama library...`);

    try {
      const res = await fetch("/api/ollama/pull", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: modelToPull })
      });
      const data = await res.json();
      alert(`Model pull status: ${data.message || 'Done'}`);
      checkSystem();
    } catch (err) {
      alert("Error pulling model: " + err.message);
    } finally {
      btnPullModel.textContent = "Pull";
      btnPullModel.disabled = false;
    }
  });

  // 5. AI Script Generation & "Thoda improve karo"
  async function handleAiScript(instruction) {
    const promptText = aiPrompt.value.trim();
    if (!promptText && instruction === "new") {
      alert("Please enter a video topic prompt (e.g. 'Compare SIP vs FD for beginners')");
      aiPrompt.focus();
      return;
    }

    const originalBtn = instruction === "new" ? btnGenerateScript : btnRefineScript;
    const originalText = originalBtn.innerHTML;
    originalBtn.innerHTML = "<span>⏳ Ollama Thinking...</span>";
    originalBtn.disabled = true;
    showStatus(`Ollama is writing script with model: ${modelSelect.value}...`);

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
        showStatus("✨ Script generated successfully! Edit it or click Render Reel.");
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

  // 6. Render Full Reel Pipeline
  btnRenderReel.addEventListener("click", async () => {
    const projectId = projectIdInput.value.trim() || "REEL_001_SIP_FD_REALITY_CHECK";
    const title = reelTitleInput.value.trim() || "SIP & FD Reality Check";
    const script = scriptContent.value.trim();
    const voice = voiceSelect.value;
    const voiceStyle = voiceStyleSelect.value;
    const captionStyle = captionStyleSelect.value;
    const burnSubtitles = burnSubtitlesCheck.checked;

    if (!script) {
      alert("Please provide a voiceover script.");
      return;
    }

    btnRenderReel.disabled = true;
    renderBtnText.textContent = "Rendering (PPTX + Slides + Neural TTS + Hormozi Captions)...";
    renderSpinner.classList.remove("hidden");
    showStatus("Step 1/3: Generating 9:16 PowerPoint Deck & Cat Meme Slides...");

    try {
      const res = await fetch("/api/render", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: projectId,
          title: title,
          script_text: script,
          voice: voice,
          voice_style: voiceStyle,
          caption_style: captionStyle,
          burn_subtitles: burnSubtitles,
          cat_theme: selectedCatTemplate
        })
      });

      const data = await res.json();
      if (data.success) {
        showStatus("🎉 Reel assembled! PowerPoint deck built & Hormozi captions burned successfully!");
        
        // Update Video Player
        const t = new Date().getTime();
        const videoUrl = `${data.video_url}?t=${t}`;
        videoSource.src = videoUrl;
        reelPlayer.load();
        videoPlaceholder.classList.add("hidden");
        
        // Update Download links
        btnDownloadMp4.href = videoUrl;
        btnDownloadMp4.download = `${projectId}_final.mp4`;
        btnDownloadPptx.href = `${data.pptx_url}?t=${t}`;
        btnDownloadPptx.download = `${projectId}_presentation.pptx`;
        btnDownloadZip.href = `${data.download_zip}?t=${t}`;
        
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
      renderBtnText.textContent = "🎬 Generate Video + PowerPoint Deck (.pptx)";
      renderSpinner.classList.add("hidden");
    }
  });

  // 7. Load Slide Thumbnails
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

  // Initialize
  checkSystem();
  loadCatTemplates();
  loadThumbnails(projectIdInput.value);
});
