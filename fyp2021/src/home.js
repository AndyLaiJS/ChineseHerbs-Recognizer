import React from "react";
import "./App.css";
import CircularPicFrame from "./components/CircularPicFrame";
import UploadButton from "./components/UploadButton";

export default function Home() {
	return (
		<div className="App">
			<CircularPicFrame img={"/MHW2102-H.png"} />
			<UploadButton />
			<footer className="footer">
				A MHW2102 FYP Project done by:
				<div>Lai Jian Shin, 1155116310</div>
				<div>Saranya Gupta, 1155116398</div>
			</footer>
		</div>
	);
}
