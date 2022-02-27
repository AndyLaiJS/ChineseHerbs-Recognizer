import styles from "./UploadButton.module.css";
import { useHistory } from "react-router-dom";

const IdentifyNext = () => {
	const history = useHistory();

	const nextChange = (e) => {
		// console.log(e);
		history.push("/");
		window.location.reload();
	};

	return (
		<div className={styles.ubutton} onClick={nextChange}>
			<p>Identify Next</p>
		</div>
	);
};

export default IdentifyNext;
