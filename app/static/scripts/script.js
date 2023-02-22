// ELEMENTS DU DOM
const yannickElt = document.getElementById("yannick");
const textElt = document.getElementById("text-container");
const btnElt = document.getElementById("btn-predict");
const btnCtnElt = document.querySelector(".btn-container")
const dropZoneElt = document.querySelector(".dropzone")
const card = document.querySelector(".card");
const againElt = document.getElementById("link-predict");
const historyElt = document.getElementById("link-history");
const linksElt = document.querySelector(".links")
const resultsElt = document.createElement("div")



// Display letters one by one
function printLetterByLetter(message, speed) {
    let i = 0;
    let interval = setInterval(function () {
        textElt.innerHTML += message.charAt(i);
        i++;
        if (i > message.length) {
            clearInterval(interval);
        }
    }, speed);
}
printLetterByLetter("Yo guys, I'm Yannick, the god of AI. Put stuffs just below, click on the window or drop the files, and I'll give you my prediction for MedNet classification. Let's go !", 35);

// Move & stop Yannick
function spinYannick() {
    yannickElt.classList.add('spin');
}

// Get results & Anim
function predict() {
    spinYannick();
    btnElt.classList.remove("active");
    btnElt.disabled = true;
    historyElt.style.display = 'none'
    textElt.innerHTML = '';
    printLetterByLetter("Yoohhooo...", 80)
    let formData = new FormData();
    // formData.append('image', yannickElt);
    fetch('/predict', {
        method: 'POST',
        body: formData
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        setTimeout(() => {
            yannickElt.classList.remove('spin');
            textElt.textContent = "";
            displayResults(data)
        }, 2000);
    });
}

//Display results
function displayResults(data) {
    console.log(data.predictions);
    console.log(data.files);
    // remove childs
    card.removeChild(btnCtnElt);
    card.removeChild(dropZoneElt);

    printLetterByLetter("It was too easy for me !", 60);
    setTimeout(() => {
        for (let index = 0; index < data.predictions.length; index++) {
            console.log(data.predictions[index]);
            textElt.innerHTML += "<p>- " + data.predictions[index] + "</p>";
        }
        againElt.style.display = "block";
        historyElt.style.display = "block";
    }, 3000);
}

function reset() {
    while (resultsElt.firstChild) {
        resultsElt.removeChild(resultsElt.firstChild);
    }
    textElt.style.minHeight = "200px";
    card.removeChild(linksElt);
    againElt.style.display = "none";
    card.appendChild(btnCtnElt);
    card.appendChild(dropZoneElt);
    card.appendChild(linksElt);
    historyElt.style.display = "block";
    textElt.innerHTML = '';
    printLetterByLetter("Yo guys, I'm Yannick, the god of AI. Put stuffs just below, click on the window or drop the files, and I'll give you my prediction for MedNet classification. Let's go !", 35);
    // Remove all files
    myDropzone.removeAllFiles();
}


function history() {
    spinYannick()
    let formDataHistory = new FormData();
    fetch('/history', {
        method: 'POST',
        body: formDataHistory
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        showHistory(data);
    });
}

async function showHistory(data) {
    try {
        card.removeChild(linksElt);
        card.removeChild(btnCtnElt);
        card.removeChild(dropZoneElt);
    } catch (DOMException) {
        console.log("exception");
    }

    console.log(data.path);
    const PATH = "/static/uploads/"
    textElt.style.minHeight = "130px";
    textElt.innerHTML = '';
    printLetterByLetter("Find my last predictions just below. Et voilà !", 70)
    historyElt.style.display = "none";
    againElt.style.display = "block";

    for (let index = 0; index < data.images.length; index++) {
        // Create elements
        divRow = document.createElement("div");
        divRow.classList.add('row-result');

        labelElt = document.createElement("p");
        labelElt.classList.add("label");
        labelElt.innerHTML = data.images[index].label;

        imgElt = document.createElement("img");
        imgElt.classList.add("img-result");
        imgElt.src = PATH + data.images[index].fileName;

        divRow.appendChild(labelElt);
        divRow.appendChild(imgElt);
        resultsElt.appendChild(divRow);
    }
    card.appendChild(resultsElt)
    card.appendChild(linksElt);

}

/*---------------------------------------// Dropzone //----------------------------------------------------- */


Dropzone.autoDiscover = false;
var myDropzone = new Dropzone(".dropzone", {
    url: "/upload",
    maxFilesize: 2, // in MB
    acceptedFiles: "image/*",
    maxFiles: 6,
    acceptedFiles: ".jpeg,.jpg,.png,.JPEG,.JPG,.PNG,.webp",
    thumbnailWidth: "20",
    accept: function (file, done) {
        console.log("uploaded");
        done();
    },
    init: function () {
        this.on("maxfilesexceeded", function (file) {
            alert("No more files please!");
        });
    }
});
myDropzone.on("success", function (file, response) {
    console.log("File uploaded: ", file);
    btnElt.classList.add("active")
    btnElt.disabled = false;
    // console.log("Server response: ", response);
});
