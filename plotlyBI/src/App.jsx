import React from "react";

// Styles 
import "./styles/App.css";

// Components

export default function App() {
    return (
        <>
        <div>
            <div className="bar-top-home">
                <div className="div-connection-seelect">
                    <div>
                        <button>Connect</button>
                    </div>
                    <div>
                        <select>
                            <option>Seelect</option>
                        </select>
                    </div>
                </div>
                <div className="div-metrics-dimensions">
                    <div>
                        <p>Dimensions</p>
                    </div>
                    <div>
                        <div>
                            <p>Metrics</p>
                        </div>
                        <div>
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    );
}