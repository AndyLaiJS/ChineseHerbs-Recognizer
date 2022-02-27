import React from "react";
import "./App.css";
import { useHistory } from "react-router-dom";
import CircularPicFrame from "./components/CircularPicFrame";
import { useSelector } from "react-redux";
import IdentifyNext from "./components/IdentifyNext";

export default function Home() {
	const history = useHistory();

	const label = useSelector((state) => state.Label);
	const desc = useSelector((state) => state.Desc);

	var dataImage = localStorage.getItem("storedimg");
	var theImg = "data:image/png;base64," + dataImage;

	if (label == "") {
		history.push("/");
	}

	return (
		<div>
			<CircularPicFrame img={theImg} />
			<div className="container">
				<div className="labelHead">{label}</div>
				<div className="contentDesc">{desc}</div>
				<IdentifyNext />
			</div>
		</div>
	);
}
