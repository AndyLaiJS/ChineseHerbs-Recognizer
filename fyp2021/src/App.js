import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

function App() {
	const [file, setFile] = useState(null);
	const [error, setError] = useState(null);

	const HandleChange = (e) => {
		let selected = e.target.files[0];

		e.preventDefault();
		const formData = new FormData();

		formData.append("file", selected);

		if (selected) {
			setFile(selected);
			setError("");
			axios
				.post("http://127.0.0.1:5000/upload", formData)
				.then(function (response, data) {
					data = response.data;
					console.log(data);
				});
		} else {
			setFile(null);
			setError("Please select an image file (png or jpg)");
		}
	};

	return (
		<div className="App">
			<form method="post" encType="multipart/form-data">
				<label>
					<input type="file" onChange={HandleChange} />
				</label>
			</form>

			<div className="output">{file && <div>SUCCESS!</div>}</div>
		</div>
	);
}

export default App;
