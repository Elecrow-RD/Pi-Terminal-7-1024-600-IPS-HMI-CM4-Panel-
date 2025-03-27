module.exports = function(RED) {
    function mpu6050(config) {
        RED.nodes.createNode(this, config);
        var node = this;

        node.on('input', function(msg) {
            const { spawn } = require('child_process');

            // 启动Python脚本
            const pythonProcess = spawn('python', ['-u', '/home/pi/myNode/mpu6050/mpu6050.py']);

            // 处理Python脚本的stdout数据
            pythonProcess.stdout.on('data', (data) => {
                // 将Python脚本的输出数据放入msg.payload中
                msg.payload = data.toString();
                node.send(msg);
            });

            // 处理Python脚本的stderr数据
            pythonProcess.stderr.on('data', (data) => {
                console.error(`stderr: ${data}`);
            });

            // Python进程结束后处理
            pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    console.error(`Python process exited with code ${code}`);
                }
            });
        });
    }
    RED.nodes.registerType("mpu6050", mpu6050);
}
