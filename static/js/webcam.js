//url:https://stackoverflow.com/questions/9533773/accessing-webcam-in-web-pages

var width = 320;
var height = 0;
var streaming = false;
var localstream = null;
var nameCount = 1;

startCameraButton.onclick = start;
takePictureButton.onclick = takepicture;

navigator.mediaDevices.enumerateDevices()
    .then(gotDevices)
    .catch(function (err) {
        console.log("An error occured while getting device list! " + err);
    });

function gotDevices(deviceInfos) {
    while (videoSelect.firstChild) {
        videoSelect.removeChild(videoSelect.firstChild);
    }

    for (var i = 0; i !== deviceInfos.length; ++i) {
        var deviceInfo = deviceInfos[i];
        var option = document.createElement('option');
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === 'videoinput') {
            option.text = deviceInfo.label || 'Camera ' + (videoSelect.length + 1);
            videoSelect.appendChild(option);
        }
    }
}

function start() {
    stopVideo();
    clearphoto();
    var videoSource = videoSelect.value;
    var constraints = {
        audio: false,
        video: { deviceId: videoSource ? { exact: videoSource } : undefined }
    };
    navigator.mediaDevices.getUserMedia(constraints).
        then(gotStream).then(gotDevices).catch(handleError);
}



function gotStream(stream) {
    localstream = stream;
    video.srcObject = stream;
    video.play();
    // Refresh button list in case labels have become available
    return navigator.mediaDevices.enumerateDevices();
}

function handleError(error) {
    console.log('navigator.getUserMedia error: ', error);
}

video.addEventListener('canplay', function (ev) {
    if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width);
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);

        streaming = true;
    }
}, false);

clearphoto();

function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);
}

function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var dataURL = canvas.toDataURL("image/jpeg", 0.95);
        //
        // create temporary link  
        var tmpLink = document.createElement('a');
        tmpLink.download = 'image.png'; // set the name of the download file 
        tmpLink.href = dataURL;

        // temporarily add link to body and initiate the download  
        document.body.appendChild(tmpLink);
        tmpLink.click();
        document.body.removeChild(tmpLink);
        //
        if (dataURL && dataURL != "data:,") {
            var fileName = generateImageName();
            fileName = fileName + ".txt"
            uploadimage(dataURL, fileName);
        } else {
            console.log("Image not available");
        }
        nameCount++;
    } else {
        clearphoto();
    }
}

function generateImageName() {
    //generate image name logic here 
    imageName = "photo" + nameCount
    return imageName;
}

function uploadimage(dataurl, filename) {
    //upload logic here ...
    return dataURL
}

function generateImageName() {
    //generate image name logic here 
    return imageName;
}

function download() {
    var image = canvas.toDataURL();
    var templink = document.createElement("a")
    var imageName = generateImageName();
    templink.download = imageName;
    img.download = image;

    document.body.appendChild(templink);
    templink.click();
    document.body.removeChild(templink);
}
function stopVideo() {
    if (localstream) {
        localstream.getTracks().forEach(function (track) {
            track.stop();
            localstream = null;
        });
    }
}

