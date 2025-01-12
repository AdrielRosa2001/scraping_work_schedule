function define_btn_search_schedule(status){
  const spinner_element = document.getElementById('spinner-div');
  const btn_search_schedule = document.getElementById('search-schedule-btn');
  const label_btn_search_schedule = document.getElementById('label-btn-search-schedule');
  if (status == "default") {
    spinner_element.classList.remove('d-flex');
    spinner_element.classList.add('d-none');
    btn_search_schedule.classList.remove('btn-warning');
    btn_search_schedule.classList.add('btn-primary');
    btn_search_schedule.disabled=false;
    label_btn_search_schedule.innerHTML = "Buscar Escala";
  } else if (status == "loading"){
    spinner_element.classList.remove('d-none');
    spinner_element.classList.add('d-flex');
    btn_search_schedule.classList.remove('btn-primary');
    btn_search_schedule.classList.add('btn-warning');
    btn_search_schedule.disabled=true;
    label_btn_search_schedule.innerHTML = "Buscando Escala...";
  } else if (status == "ready"){
    spinner_element.classList.remove('d-flex');
    spinner_element.classList.add('d-none');
    btn_search_schedule.classList.remove('btn-warning');
    btn_search_schedule.classList.remove('btn-primary');
    btn_search_schedule.classList.add('btn-success');
    btn_search_schedule.disabled=true;
    label_btn_search_schedule.innerHTML = "Escala sincronizada!";
  }
}


const get_schedule = async (data) => {
  define_btn_search_schedule("loading");
  const response = await fetch('/get_schedule_nice_platform', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data)
  });
  const html = await response.text();
  if (response.status == 200){
    define_btn_search_schedule("ready");
    alert('Escala sincronizada com sucesso!')
  } else if (response.status == 401) {
    define_btn_search_schedule("default");
    alert('Usuário ou senha inválido!')
  } else {
    define_btn_search_schedule("loading");
    alert(`Falha na busca!\nError:\n${html}`)
  }
}


// Google account button
const btn_google_account = document.getElementById("btn-google-account");
btn_google_account.addEventListener("click", function (e) {
    btn_google_account.classList.remove("btn-danger");
    btn_google_account.classList.add("btn-success");
    btn_google_account.disabled=true;
    btn_google_account.innerHTML = "Conta connectada!";
  });

// Search schedule button
const form_search_schedule = document.getElementById("form-search-schedule");
form_search_schedule.addEventListener("submit", function (e) {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  get_schedule(data);
});