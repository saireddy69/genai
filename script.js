document.getElementById("analyzeBtn").addEventListener("click", async function () {

    const resumeText = document.getElementById("resumeText").value.trim();
    const loading = document.getElementById("loading");
    const resultDiv = document.getElementById("result");

    // Prevent empty submit
    if (!resumeText) {
        alert("Please paste resume text.");
        return;
    }

    // Show loading
    loading.style.display = "block";
    resultDiv.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resume_text: resumeText
            })
        });

        const data = await response.json();

        loading.style.display = "none";

        if (data.status !== "success") {
            resultDiv.innerHTML = `<p style="color:red;">${data.message}</p>`;
            return;
        }

        const resume = data.data;


        // Display formatted result
        resultDiv.innerHTML = `
            <h3>Name:</h3> <p>${resume.name || "N/A"}</p>
            <h3>Email:</h3> <p>${resume.email || "N/A"}</p>
            <h3>Skills:</h3> <ul>${(resume.skills || []).map(skill => `<li>${skill}</li>`).join("")}</ul>
            <h3>Years of Experience:</h3> <p>${resume.years_of_experience ?? "N/A"}</p>
            <h3>Education:</h3> <ul>${(resume.education || []).map(edu => `<li>${edu}</li>`).join("")}</ul>
            <h3>Summary:</h3> <p>${resume.summary || "N/A"}</p>
        `;

    } catch (error) {
        loading.style.display = "none";
        resultDiv.innerHTML = `<p style="color:red;">Something went wrong.</p>`;
    }
});
