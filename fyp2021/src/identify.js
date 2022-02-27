import React from "react";
import "./App.css";
import { useHistory } from "react-router-dom";
import CircularPicFrame from "./components/CircularPicFrame";
import { useSelector } from "react-redux";

export default function Home() {
	const history = useHistory();

	const label = useSelector((state) => state.Label);
	const desc = useSelector((state) => state.Desc);

	var dataImage = localStorage.getItem("storedimg");
	var theImg = "data:image/png;base64," + dataImage;

	if (label == "") {
		history.push("/");
	}

	const nextChange = (e) => {
		// console.log(e);
		history.push("/");
		window.location.reload();
	};

	return (
		<div>
			<CircularPicFrame img={theImg} />
			<div className="container">
				<div className="labelHead">{label}</div>
				<div className="contentDesc">{desc}</div>
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
