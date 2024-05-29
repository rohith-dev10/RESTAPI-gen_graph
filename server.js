const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors({
    origin: "*",
    methods: ["GET", "POST"],
}));
app.use(bodyParser.json());

app.get("/",(req,res)=>{
    res.json({"result":"Success!"})
})

app.post("/generate-plot", (req, res) => {
    const inputData = req.body;

    const pythonProcess = spawn("python", ["plot.py"]);

    pythonProcess.stdin.write(JSON.stringify(inputData));
    pythonProcess.stdin.end();

    let dataChunks = [];
    pythonProcess.stdout.on("data", (chunk) => {
        dataChunks.push(chunk);
    });

    pythonProcess.stdout.on("end", () => {
        const base64Image = Buffer.concat(dataChunks).toString();
        console.log(base64Image);
        res.json({ image: base64Image });
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        res.json({ "error": data })
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
