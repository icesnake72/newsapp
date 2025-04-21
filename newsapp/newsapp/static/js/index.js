function goToCategory(select) {
  const categoryId = select.value;
  if (categoryId) {
    window.location.href = `/category/${categoryId}/`;  // 선택된 카테고리로 이동
  } else {
    window.location.href = `/`;  // 전체 보기
  }
}

let mediaRecorder;
let ws;


function onRecordButtonClick() {
  const recordButton = document.getElementById('recordButton');
  const recordButtonText = recordButton.innerText;
  if (recordButtonText === '녹음 시작') {
    recordButton.innerText = '녹음 중지';
    startRecording();
  } else {
    recordButton.innerText = '녹음 시작';
    stopRecording();
  }
}


function startRecording() {
  ws = new WebSocket("ws://localhost:8000/ws/audio/");
  ws.binaryType = "arraybuffer";

  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      mediaRecorder.ondataavailable = event => {
        const audioBlob = event.data;
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
      };
    })
    .catch(error => {
      console.error('Error accessing the microphone:', error);
    });
}

function stopRecording() {
  // 녹음 중지
  mediaRecorder.stop();
}