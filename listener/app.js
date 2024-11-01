const express = require("express");
const WebSocket = require("ws");
const http = require("http");

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const port = 2399;

app.get("/", (req, res) => {
  res.status(200).json({ message: "Hello World!" });
});

wss.on("connection", (ws) => {
  console.log("Novo cliente conectado");

  ws.on("message", (message) => {
    console.log(`Mensagem python: ${message}`);
  });

  ws.on("close", () => {
    console.log("Cliente desconectado");
  });
});

server.listen(port, () => {
  console.log("App listening on port: ", port);
});
