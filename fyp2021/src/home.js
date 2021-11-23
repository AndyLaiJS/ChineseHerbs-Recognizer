import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import "./App.css";
import axios from "axios";

export default function Home() {
	const history = useHistory();
	const [content, setContent] = useState(null);
	const [file, setFile] = useState(null);

	// This some Dr. Strange stuff
	function getBase64Image(img) {
		var canvas = document.createElement("canvas");
		canvas.width = img.width;
		canvas.height = img.height;
		var ctx = canvas.getContext("2d");
		ctx.drawImage(img, 0, 0);
		var dataURL = canvas.toDataURL("image/jpeg");
		return dataURL.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
	}

	// once content is filled, go to /identified page carrying the content data
	useEffect(() => {
		if (content != null) {
			history.push({
				pathname: "/identified",
				state: {
					Label: content.label,
					Desc: content.data,
				},
			});
		}
	}, [content]);

	const HandleChange = (e) => {
		let selected = e.target.files[0];

		// prepare the img for localStorage
		var img = new Image();
		img.src = URL.createObjectURL(selected);
		var imgData = null;

		// once img is loaded, run this function
		img.onload = function () {
			imgData = getBase64Image(img);
			var ib = Buffer.from(imgData, "base64");
			// console.log(imgData); // imgData is our base64 encoding
			var length = imgData.length;
			var imageBytes = new ArrayBuffer(length);
			var ua = new Uint8Array(imageBytes);
			for (var i = 0; i < length; i++) {
				ua[i] = imgData.charCodeAt(i);
			}
			// store it somewhere for identity.js to read
			localStorage.setItem("storedimg", imgData);
		};

		e.preventDefault();
		// preparing the img into a FormData format so Flask backend can process it
		const formData = new FormData();

		formData.append("file", selected);

		// for Flask to handle
		if (selected) {
			setFile(selected);
			axios
				.post("http://127.0.0.1:5000/upload", formData)
				.then(function (response, data) {
					data = response.data;
					setContent(data);
					console.log(data);
				});

			const reader = new FileReader();
			// reader.addEventListener("load", () => {
			// 	setImgData(reader.result);
			// });
			reader.readAsDataURL(e.target.files[0]);
		} else {
			setFile(null);
		}
	};

	return (
		<div className="App">
			<div className="bCircle">
				<div className="fCircle">
					<img className="upl_img" src="/MHW2102.png" />
				</div>
			</div>
			<div className="label">
				{file && content && <div>{content.label}</div>}
			</div>
			<div className="desc">{file && content && <div>{content.data}</div>}</div>
			<form method="post" encType="multipart/form-data">
				<label>
					<input type="file" onChange={HandleChange} />
					<span className="ubutton">
						<div className="b_inside">
							<p
								style={{
									fontSize: "28px",
									fontWeight: "bolder",
									color: "#FF4689",
									margin: "0",
								}}
							>
								Upload
							</p>
						</div>
					</span>
				</label>
			</form>
			<div className="footer">
				A MHW2102 FYP Project done by:
				<div>Lai Jian Shin, 1155116310</div>
				<div>Saranya Gupta, 1155116398</div>
			</div>
		</div>
	);
}
