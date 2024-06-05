const inputs_obrigatorios = document.querySelectorAll('[required]');
const formulario = document.querySelector('[data-formulario]');

formulario.addEventListener('submit', (e) => {
    e.preventDefault(); // deixa de executar o comando normal do botao
    
    const lista_inputs_form = {};
    inputs_obrigatorios.forEach(input => {
        lista_inputs_form[input.name] =  input.value; // para cada input obtem o valor e coloca na lista
    });
    
    // salva os dados no localstorage para a proxima pagina
    localStorage.setItem('registro', JSON.stringify(lista_inputs_form));
    window.location.href = 'verificacao_facial'; // envia para a pagina de verificacao facial
});