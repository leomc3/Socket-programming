# Socket-programming
Redes - multi cliente servidor

Universidade do Minho
REDES, Especialização em Segurança Cibernética - Turma I (2024)
Prof. Flávio de Oliveira Silva, Ph.d.
Laboratório 02 – Socket Programming
As aplicações que geralmente utilizamos utilizam a rede, em particular a Internet, para a
transmissão de dados entre diferentes máquinas.
De maneira simples, a comunicação entre aplicações, é a comunicação entre diferentes
processos de software em execução em diferentes máquinas com capacidade de
processamento. Estas máquinas podem ser reais (físicas) ou virtuais e que estão
executando em algum ponto, conectadas por uma rede.
Para a comunicação entre processos, o sistema operacional, oferece o recurso de sockets
que permitem a utilização de pilha TCP/IP para a comunicação entre diferentes processos
em execução simultânea em diferentes máquinas.
O objetivo deste laboratório é utilizar a interface de programação em sockets (Sockets
Programming) para a construção de uma aplicação baseada em sockets.
Neste laboratório, um dos processos será o servidor (server) e outros processos se
comportarão como os os clientes (cliente) que vão consumir serviços deste servidor. A
comunicação entre o cliente o servidor será feita utilizando o protocolo TCP.
Para realização do laboratório você precisará de escolher uma linguagem de programação
e ter um ambiente adequado (IDE, DEBUG, etc.) para a criação do código do cliente, dos
servidores e ainda sua posterior execução e ainda a inspeção os dados através da rede
utilizando o Wireshark
O servidor será responsável pela troca de mensagens de texto entre diversos clientes
simultaneamente conectados.
Considere que há um protocolo chamado CHAT-MSG e que será responsável pela troca de
mensagens entre o servidor e os clientes da seguinte forma:
Tabela 1 - Serviços Básicos do Protocolo
SERVIÇO Sintaxe e Formato
Envia uma mensagem de texto para um determinado cliente MSG client-id text
Envia uma mensagem de texto para todos os clientes
conectados
MSG ALL text
Realiza o login de um novo cliente LOGIN client-id
Realiza o logoff de um cliente do chat LOGOFF client-id
Outro Serviço a ser definido... Sintaxe e formato TBD...
Universidade do Minho
REDES, Especialização em Segurança Cibernética - Turma I (2024)
Prof. Flávio de Oliveira Silva, Ph.d.
Algumas considerações que devem ser levadas em conta ao criar o comportamento do
servidor e dos clientes:
• O servidor deve suportar múltiplos clientes de forma simultânea
• Todas as mensagens trocadas entre os clientes devem passar primeiro no servidor. O
servidor é o responsável por encaminhar as mensagens para um determinado cliente
• O cliente e o servidor devem utilizar somente a biblioteca básica de Socket oferecida pelo
sistema operacional e suportada por diversas linguagens de programação
• O servidor deve receber pela linha de comando a porta que vai utilizar em sua operação
• O cliente deve receber pela linha de comando o endereço IP e a porta do servidor
O trabalho envolve:
1) Criar o código do servidor e do cliente conforme as especificações mostradas acima
2) Detalhar os cenários de testes dos diversos serviços do protocolo e realizá-los através da
linha de comando com a correspondente coleta das evidências de execução e
funcionamento. Neste caso, para os testes considerar que o servidor e clientes estão
executando localmente. Neste caso utilizar o IP de loopback. (127.0.0.1).
3) Após o serviço testado e em funcionamento como esperado, ativar o Wireshark para
captura de pacotes. Durante a captura, utilize cada um dos serviços criados. Assim
posteriormente será possível inspecionar o conteúdo do dados trafegados e realizar uma
análise que mostre cada serviço invocado e os dados transferidos na rede associados a
este serviço. Neste caso utilizar ao menos um cliente em com um IP em uma rede local
sem fio e ainda, é necessário que o servidor esteja acessível remotamente via a Internet.
Uma possibilidade aqui é criar uma VM no Azure com o código de seu servidor instalado.
4) Ativar o Wireshark para captura de pacotes; iniciar cinco (5) diferentes clientes e enviar
uma mensagem de texto simultânea para estes clientes. Salvar os dados da captura e
incluir no relatório uma análise dos dados transferidos e sua relação com a operação
realizada na aplicação. Neste caso utilizar cada um dos clientes com diferentes IPs e um
servidor acessível remotamente via a Internet. Para simular os diversos clientes é possível
utilizar VMs criadas em seu equipamento, conectar algum outro computador físico via
rede sem fio ou ainda realizar o teste utilizando de forma simultânea Outra opção pode
ser os computadores físicos dos membros dos grupos utilizados ao mesmo tempo.
5) Propor um novo serviço para este protocolo. O comportamento deste novo serviço, assim
como a sintaxe e formato da mensagem são livres. O serviço deve ter relação com o
contexto geral, troca de mensagens de texto entre clientes.
6) Caso o novo serviço envolva o uso de mecanismos de criptografia, este item conterá
pontuação extra, além do previsto para o Item 5 sem o uso de criptografia. Exemplos de
serviços: autenticação de usuários, mensagens troca de mensagens cifradas, etc.
Este laboratório será realizado em grupo, com até cinco (5) participantes. Ao final da
atividade o grupo deve preparar um relatório sobre a atividade acima.
Universidade do Minho
REDES, Especialização em Segurança Cibernética - Turma I (2024)
Prof. Flávio de Oliveira Silva, Ph.d.
O relatório deverá conter a seguinte estrutura:
1. Introdução
2. Desenvolvimento
2.1. Visão Geral do Cliente e Servidor
2.2. Testes Básicos de Funcionalidades
2.3. Troca de Mensagens Entre Clientes com Servidor Remoto – Visão das Camadas com
Wireshark – Nesta seção identificar as mensagens do seu protocolo, juntamente com o
seu cabeçalho e PDU. Também identificar e analisar os cabeçalhos e PDUs dos outros
protocolos da pilha utilizados na comunicação.
2.4. Troca de Mensagens Entre Clientes com Rede sem Fio e Servidor Remoto – Visão das
Camadas com Wireshark – Nesta seção identificar as mensagens do seu protocolo,
juntamente com o seu cabeçalho e PDU. Também identificar e analisar os cabeçalhos e
PDUs dos outros protocolos da pilha utilizados na comunicação. Ainda no texto desta
seção, detalhar o cenário de teste que foi utilizado para a captura.
2.5. Troca de Mensagens Entre Clientes Simultâneos com Servidor Remoto – Visão das
Camadas com Wireshark – Nesta seção identificar as mensagens do seu protocolo,
juntamente com o seu cabeçalho e PDU. Também identificar e analisar os cabeçalhos e
PDUs dos outros protocolos da pilha utilizados na comunicação. Ainda no texto desta
seção, detalhar o cenário de teste que foi utilizado para a captura.
2.6. Novo Serviço Proposto – Nesta seção detalhar e explicar o funcionamento do novo
serviço.
2.7. Testes e Evidências deste Novo Serviço – Visão das Camadas com Wireshark – Nesta seção
identificar as mensagens do seu protocolo, juntamente com o seu cabeçalho e PDU.
Também identificar e analisar os cabeçalhos e PDUs dos outros protocolos da pilha
utilizados na comunicação.
3. Conclusão
3.1. Desafios e Lições Aprendidas
No relatório o grupo deve descrever em linhas gerais como o seu código e como foi
estruturada a solução destacando exemplos do seu próprio código. O relatório poderá ser
criado da maneira o que entender ser mais conveniente. No final deve ser gerado um PDF.
Na entrega o grupo deve anexar no TEAMS: relatório, código-fonte do cliente e servidor e
ainda a coleta de dados realizada com o Wireshark.
A entrega será até o dia 05/08/2024 (segunda-feira).
Universidade do Minho
REDES, Especialização em Segurança Cibernética - Turma I (2024)
Prof. Flávio de Oliveira Silva, Ph.d.
Referências
• Simple Chat Room using Python
• PyCryptodome - Python package of low-level cryptographic primitives
• PyCryptodome - Examples
• Microsoft Azure for Students – Crédito de Conta Gratuita | Microsoft Azure
