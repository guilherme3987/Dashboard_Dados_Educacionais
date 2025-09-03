document.addEventListener('DOMContentLoaded', function() {
    const btnMostrarMais = document.getElementById('btn-mostrar-mais');
    const tabelaCorpo = document.getElementById('tabela-corpo');
    const registrosExibidosSpan = document.getElementById('registros-exibidos');
    const totalRegistros = parseInt('{{ total_registros }}');
    let registrosAtuais = parseInt('{{ dados|length }}');

    if (btnMostrarMais) {
        btnMostrarMais.addEventListener('click', function() {
            console.log('Botão "Mostrar Mais Linhas" clicado.');
            btnMostrarMais.disabled = true;
            btnMostrarMais.textContent = 'Carregando...';

            fetch('/mais_dados')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro na resposta do servidor: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(dados => {
                    if (dados.erro) {
                        console.error('Erro ao carregar mais dados:', dados.erro);
                        alert('Erro ao carregar mais dados: ' + dados.erro);
                    } else {
                        dados.forEach(linha => {
                            const novaLinha = document.createElement('tr');
                            novaLinha.className = 'border-b border-slate-700 hover:bg-slate-700/50 transition-colors duration-150';
                            
                            for (const chave in linha) {
                                if (linha.hasOwnProperty(chave)) {
                                    const novoTd = document.createElement('td');
                                    novoTd.className = 'px-6 py-4 whitespace-nowrap';
                                    novoTd.textContent = linha[chave];
                                    novaLinha.appendChild(novoTd);
                                }
                            }
                            tabelaCorpo.appendChild(novaLinha);
                        });

                        registrosAtuais += dados.length;
                        registrosExibidosSpan.textContent = registrosAtuais;
                        btnMostrarMais.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Erro de requisição:', error);
                    alert('Erro de conexão ao carregar os dados. Verifique o console para mais detalhes.');
                })
                .finally(() => {
                    btnMostrarMais.disabled = false;
                    btnMostrarMais.textContent = 'Mostrar Mais Linhas';
                });
        });

        if (registrosAtuais >= totalRegistros) {
            btnMostrarMais.style.display = 'none';
        }
    }
});


        // Sistema de tabs
        document.querySelectorAll('.tab-btn').forEach(button => {
            button.addEventListener('click', () => {
                // Remover classe ativa de todos os botões e conteúdos
                document.querySelectorAll('.tab-btn').forEach(btn => {
                    btn.classList.remove('text-emerald-300', 'border-emerald-400');
                    btn.classList.add('text-slate-400');
                });
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Adicionar classe ativa ao botão clicado e conteúdo correspondente
                button.classList.remove('text-slate-400');
                button.classList.add('text-emerald-300', 'border-b-2', 'border-emerald-400');
                document.getElementById(button.dataset.tab).classList.add('active');
            });
        });
        
        // Carregar mais dados
        document.addEventListener('DOMContentLoaded', function() {
            const btnMostrarMais = document.getElementById('btn-mostrar-mais');
            const tabelaCorpo = document.getElementById('tabela-corpo');
            const registrosExibidosSpan = document.getElementById('registros-exibidos');
            const totalRegistros = parseInt('{{ total_registros }}');
            let registrosAtuais = parseInt('{{ dados|length }}');

            if (btnMostrarMais) {
                btnMostrarMais.addEventListener('click', function() {
                    btnMostrarMais.disabled = true;
                    btnMostrarMais.textContent = 'Carregando...';

                    fetch('/mais_dados')
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Erro na resposta do servidor: ' + response.statusText);
                            }
                            return response.json();
                        })
                        .then(dados => {
                            if (dados.erro) {
                                console.error('Erro ao carregar mais dados:', dados.erro);
                                alert('Erro ao carregar mais dados: ' + dados.erro);
                            } else {
                                dados.forEach(linha => {
                                    const novaLinha = document.createElement('tr');
                                    novaLinha.className = 'border-b border-slate-700 hover:bg-slate-700/50 transition-colors duration-150';
                                    
                                    for (const chave in linha) {
                                        if (linha.hasOwnProperty(chave)) {
                                            const novoTd = document.createElement('td');
                                            novoTd.className = 'px-6 py-4 whitespace-nowrap';
                                            novoTd.textContent = linha[chave];
                                            novaLinha.appendChild(novoTd);
                                        }
                                    }
                                    tabelaCorpo.appendChild(novaLinha);
                                });

                                registrosAtuais += dados.length;
                                registrosExibidosSpan.textContent = registrosAtuais;
                                
                                if (registrosAtuais >= totalRegistros) {
                                    btnMostrarMais.style.display = 'none';
                                }
                            }
                        })
                        .catch(error => {
                            console.error('Erro de requisição:', error);
                            alert('Erro de conexão ao carregar os dados. Verifique o console para mais detalhes.');
                        })
                        .finally(() => {
                            btnMostrarMais.disabled = false;
                            btnMostrarMais.textContent = 'Mostrar Mais Linhas';
                        });
                });

                if (registrosAtuais >= totalRegistros) {
                    btnMostrarMais.style.display = 'none';
                }
            }
        });