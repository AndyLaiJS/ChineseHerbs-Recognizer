import React, { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import { useHistory, useLocation } from "react-router-dom";

export default function Home() {
	const history = useHistory();
	const location = useLocation();
	const [content, setContent] = useState(null);
	const [file, setFile] = useState(null);
	const [imgData, setImgData] = useState(null);

	var dataImage = localStorage.getItem("storedimg");
	var theImg = "data:image/png;base64," + dataImage;

	useEffect(() => {
		console.log(location.state);
	}, [location]);

	const nextChange = (e) => {
		// console.log(e);
		history.push("/");
		window.location.reload();
	};

	return (
		<div>
			<div className="bCircle">
				<div className="fCircle">
					<img className="fill_img" src={theImg} />
				</div>
			</div>
			<div className="container">
				<div className="labelHead">{location.state.Label}</div>
				<div className="contentDesc">{location.state.Desc}</div>
				<div className="ubutton" onClick={nextChange}>
					<div className="b_inside">
						<p
							style={{
								fontSize: "28px",
								fontWeight: "bolder",
								color: "#FF4689",
								margin: "0",
							}}
						>
							Identify Next
						</p>
					</div>
				</div>
			</div>
		</div>
	);
}
