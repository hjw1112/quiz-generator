document.addEventListener("DOMContentLoaded", function () {
    const methodSelect = document.getElementById("method");
    const fileUpload = document.getElementById("fileUpload");
    const topicInput = document.getElementById("topicInput");

    methodSelect.addEventListener("change", function () {
        if (this.value === "file") {
            fileUpload.style.display = "block";
            topicInput.style.display = "none";
        } else {
            fileUpload.style.display = "none";
            topicInput.style.display = "block";
        }
    });


    document.getElementById("input_button").addEventListener("click", function () {
        document.getElementById("file_upload").click();
    });

    document.getElementById("file_upload").addEventListener("change", function () {
        let fileName = this.files.length > 0 ? this.files[0].name : "No file selected";
        document.getElementById("file_name").textContent = fileName;
    });



    document.getElementById("form").addEventListener("submit", function (e) {
        e.preventDefault();

        let formData = new FormData();
        formData.append("method", methodSelect.value);

        if (methodSelect.value === "file") {
            let file_input = document.getElementById("file_upload");
            if (!file_input) {
                alert("Please upload a file.");
                return;
            }
            formData.append("file", file_input.files[0]);
        } else {
            let topic = document.getElementById("topic").value;
            if (!topic) {
                alert("Please enter a topic.");
                return;
            }
            formData.append("topic", topic);
        }
        loader.style.display = 'block';

        fetch("/generate", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                console.error("Error: No redirect URL provided");
            }
        })
        .catch(error => console.error("Error:", error));
        
    });
});
