module.exports = function(RED) {

    function max30102(config) {
        RED.nodes.createNode(this, config);

        var node = this;

        node.on('input', function(msg) {
            const { spawn } = require('child_process');

            if (msg.payload === true) {
                console.error(`Start max30102 script!!`);
                const pythonProcess = spawn('python', ['-u', '/home/pi/myNode/max30102/MAX30102/max30102_main.py']);
                // 处理Python脚本的stdout数据
                pythonProcess.stdout.on('data', (data) => {
                // 将Python脚本的输出数据放入msg.payload中
                msg.payload = data.toString();
                node.send(msg);
                });

                // 处理python脚本的stderr错误
                pythonProcess.stderr.on('data', (data)=> {
                console.error(`stderr:${data}`);
                node.error(`python process error happended-->${data}`);
                });

                // Python进程结束后处理
                pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    console.error(`Python process exited with code ${code}`);
                }
                });
            } else {
                console.error(`Stop max30102 script!!`);
                const { exec } = require('child_process');
                const command = 'ps -ef | grep max30102_main.py | grep -v grep | cut -c 9-16 | xargs kill -s 2';
                exec(command, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error executing command: ${error.message}`);
                        return;
                    }

                    if (stderr) {
                        console.error(`stderr: ${stderr}`);
                        return;
                    }
                });
                // node.error(`Stop pulse script!`);
            }
            
        });
    }
    RED.nodes.registerType("max30102", max30102);
}