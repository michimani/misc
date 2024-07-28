import { useState } from "react";
import { getHealth } from "./services/health";
import "./App.css";

function App() {
	const [healthStatus, setHealthStatus] = useState<string | null>(null);
	const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

	const healthCheck = async () => {
		await getHealth()
			.then((data) => {
				setHealthStatus(data);
				setIsHealthy(true);
			})
			.catch((error) => {
				setHealthStatus(`Error fetching health data.\n\n(detail: ${error})`);
				setIsHealthy(false);
			});
	};

	return (
		<>
			<h1>Vite + React with HTTP API Server in Go</h1>
			<div className="card">
				<button type="button" onClick={healthCheck}>
					Check HTTP API Server
				</button>
				<p>
					<span
						style={{
							color:
								isHealthy === null
									? "transparent"
									: isHealthy
										? "lightgreen"
										: "lightcoral",
							marginRight: "0.5rem",
						}}
					>
						●
					</span>
					{healthStatus === null
						? "Click the button to check the health status"
						: healthStatus}
				</p>
			</div>
		</>
	);
}

export default App;
