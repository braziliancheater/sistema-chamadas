const container_camera = document.querySelector('[data-camera]');
const objeto_camera = document.querySelector('[data-video]');

let url_imagem = '';

/*
    Abre a câmera do usuário e exibe na tela
*/
const abrir_camera_button = document.querySelector('[data-video-botao]');
abrir_camera_button.addEventListener('click', async (e) => {
    // usuario precisa permitir o acesso a camera
    try {
        const getWebcam = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        objeto_camera.srcObject = getWebcam;
    
        abrir_camera_button.style.display = 'none';
        container_camera.style.display = 'block';
    }
    catch (err) {
        const mensagem_erro = document.querySelector('[data-mensagem-erro]');
        mensagem_erro.innerText = 'Você precisa conceder o acesso a sua câmera. Por favor, verifique as configurações do seu navegador e recarregue a página.';
        console.log(err);
    }
});

/*
Mostra a imagem capturada na tela e salva no localStorage
*/
const container_foto = document.querySelector('[data-mensagem]'); 
const elemento_canvas = document.querySelector('[data-video-canvas]'); 
const tirar_foto_button = document.querySelector('[data-tirar-foto]');
const imagemInput = document.querySelector('#foto');
const nomeInput = document.querySelector('#nome');
const emailInput = document.querySelector('#email');
const senhaInput = document.querySelector('#senha');
const raInput = document.querySelector('#ra');
tirar_foto_button.addEventListener('click', () => {
    // create an image based on current frame of the webcam
    elemento_canvas.getContext('2d').drawImage(objeto_camera, 0, 0, elemento_canvas.width, elemento_canvas.height);

    // save image as JPEG
    url_imagem = elemento_canvas.toDataURL('image/jpeg');

    container_camera.style.display = 'none';
    container_foto.style.display = 'block';

    imagemInput.value = url_imagem;
    const localData = JSON.parse(localStorage.getItem('registro'));
    nomeInput.value = localData.nome;
    emailInput.value = localData.email;
    raInput.value = localData.ra;
    senhaInput.value = localData.password;
});

/*
    Salva a imagem no localStorage
*/
const elemento_formulario = document.querySelector('[data-enviar]'); // obtem o formulario
elemento_formulario.addEventListener('click', () => {
    const localData = JSON.parse(localStorage.getItem('registro')); // obtem o objeto do localStorage
    
    localData.image =  url_imagem; // adiciona uma nova propriedade ao objeto
    localStorage.setItem('registro', JSON.stringify(localData)); // atualiza o objeto no localStorage
})

/*
Refaz a foto
*/
const refazer_foto_button = document.querySelector('[data-refazer-foto]');
refazer_foto_button.addEventListener('click', () => {
    container_foto.style.display = 'none';
    container_camera.style.display = 'block';
});