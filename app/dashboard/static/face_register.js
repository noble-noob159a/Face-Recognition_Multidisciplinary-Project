document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  const registerName = document.getElementById("registerName");
  const registerImage = document.getElementById("registerImage");
  const imagePreviewContainer = document.getElementById("imagePreviewContainer");
  const imagePreview = document.getElementById("imagePreview");
  const registerSubmit = document.getElementById("registerSubmit");
  const registerMessage = document.getElementById("registerMessage");

  let previewUrl = null;

  registerImage.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
      previewUrl = URL.createObjectURL(file);
      imagePreview.src = previewUrl;
      imagePreviewContainer.classList.remove("hidden");
    } else {
      clearPreview();
    }
  });

  function clearPreview() {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      previewUrl = null;
    }
    imagePreview.removeAttribute("src");
    imagePreviewContainer.classList.add("hidden");
  }

  function showMessage(text, isError) {
    registerMessage.textContent = text;
    registerMessage.className = "text-sm font-medium p-3 rounded-md " + 
      (isError ? "bg-red-100 text-red-700" : "bg-emerald-100 text-emerald-700");
    registerMessage.classList.remove("hidden");
  }

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    registerMessage.classList.add("hidden");
    
    const file = registerImage.files[0];
    const name = registerName.value.trim();
    
    if (!name || !file) {
      showMessage("Name and image are required.", true);
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("image", file);

    registerSubmit.disabled = true;
    registerSubmit.textContent = "Registering...";

    try {
      // Use API_URL from env config if available, otherwise fallback to relative
      const baseUrl = window.API_URL || "";
      const apiUrl = `${baseUrl}/api/register`;
      
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "An error occurred during registration.");
      }

      showMessage(`Registered successfully: ${data.name}`, false);
      registerForm.reset();
      clearPreview();
    } catch (err) {
      showMessage(err.message, true);
    } finally {
      registerSubmit.disabled = false;
      registerSubmit.textContent = "Register";
    }
  });
});
