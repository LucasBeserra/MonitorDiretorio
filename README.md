# MonitorDiretorio
Um serviço para windows desenvolvido em python que monitora todos os eventos do diretório especificado e registra em um arquivo de log com data, hora e tipo de evento. Dessa forma, além de poder rastrear os arquivos da pasta, é possível importar o arquivo log para excel e ter insights cronológicos do histórico das movimentação, sabendo quando (e se) o os eventos aconteceram tal como a quantidade de movimentações realizadas e a distribuição desses ao longo do tempo. 

Tecnologias utilizadas: 
Biblioteca watchdog: para capturar e responder a eventos dentro do diretório; 
Biblioteca pywin32: para rodar a aplicação como serviço do windows.
