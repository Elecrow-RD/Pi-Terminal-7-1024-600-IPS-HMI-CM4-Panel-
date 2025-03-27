module.exports = function(RED) {

    function pca9557(config) {

        RED.nodes.createNode(this, config);

        var node = this;

        node.initOnce = function() {
            if(!node.initialized) {
                const { spawn } = require('child_process');
                const pythonProcess = spawn('python', ['-u', '/home/pi/myNode/pca9557/pca9557Init.py']);
                node.initialized = true;

                pythonProcess.stderr.on('data', (data) => {
                    node.error(`stderr: ${data}`);
                });

                pythonProcess.on('close', (code) => {
                    if (code !== 0) {
                        node.error(`Python initialization process exited with code ${code}`);
                    }
                });
            }
        };

        node.initOnce();

        this.outputmsgs = config.outputmsgs;

        node.on('input', function(msg) {
            const { spawn } = require('child_process');

            // 从msg.payload中获取参数
            const outputmsgs = msg.outputmsgs;
            const pin = msg.outputmsgs.pin;
            const val = msg.outputmsgs.val;
                        
            // console.error(`pin[${pin}], value[${val}]`)
            const pythonProcess = spawn('python', ['-u', '/home/pi/myNode/pca9557/pca9557.py', pin, val]);

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
    RED.nodes.registerType("pca9557", pca9557);
}
