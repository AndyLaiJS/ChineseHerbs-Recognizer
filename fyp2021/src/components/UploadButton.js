import styles from "./UploadButton.module.css";
import { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { useDispatch } from "react-redux";
import { recognizerActions } from "../store/redux_index";

const UploadButton = () => {
	const history = useHistory();
	const [content, setContent] = useState(null);
	const dispatch = useDispatch();

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
			dispatch(
				recognizerActions.updateStore({
					label: content.label,
					desc: content.data,
				})
			);
			history.push("/identified");
		}
	}, [content]);

	const HandleChange = (e) => {
		e.preventDefault();

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

		// preparing the img into a FormData format so Flask backend can process it
		const formData = new FormData();
		console.log(selected);

		formData.append("file", selected);

		// for Flask to handle
		if (selected) {
			axios
				.post("http://127.0.0.1:5000/upload", formData)
				.then(function (response, data) {
					data = response.data;
					setContent(data);
					console.log(data);
				})
				.catch(function (error) {
					console.log(error);
				});

			const reader = new FileReader();
			reader.readAsDataURL(e.target.files[0]);
		}
	};

	return (
		<form method="post" encType="multipart/form-data">
			<label>
				<input type="file" onChange={HandleChange} />
				<span className={styles.ubutton}>
					<p>Upload</p>
				</span>
			</label>
		</form>
	);
};

export default UploadButton;
