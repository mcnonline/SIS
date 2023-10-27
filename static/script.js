function alterarStatus(porta) {
    if (porta.classList.contains("vazio")) {
        porta.classList.remove("vazio");
        porta.classList.add("ocupado");
    } else {
        porta.classList.remove("ocupado");
        porta.classList.add("vazio");
    }
}
