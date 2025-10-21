import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "SimpleCSVParser.FileBrowser",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "SimpleCSVParser") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                // Find the csv_file_path widget
                const pathWidget = this.widgets.find(w => w.name === "csv_file_path");

                if (pathWidget) {
                    // Create a button widget to browse for files
                    const browseButton = this.addWidget("button", "Browse...", null, () => {
                        // Create a file input element
                        const fileInput = document.createElement("input");
                        fileInput.type = "file";
                        fileInput.accept = ".csv";

                        // Handle file selection
                        fileInput.onchange = (e) => {
                            if (e.target.files && e.target.files[0]) {
                                const file = e.target.files[0];
                                // Get the file path (this will be the file name in browser)
                                // For local file paths, we'll use the path API if available
                                if (file.path) {
                                    // Electron environment (desktop ComfyUI)
                                    pathWidget.value = file.path;
                                } else {
                                    // Browser environment - show filename with instruction
                                    pathWidget.value = file.name;
                                    alert("Note: In browser mode, please enter the full file path manually.\nFile selected: " + file.name);
                                }
                            }
                        };

                        // Trigger file browser
                        fileInput.click();
                    });
                }

                return r;
            };
        }
    }
});
