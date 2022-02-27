import styles from "./CircularPicFrame.module.css";
const CircularPicFrame = (props) => {
	return (
		<div className={styles.bCircle}>
			<div className={styles.fCircle}>
				<img
					className={
						props.img == "/MHW2102.png" ? styles.upl_img : styles.fill_img
					}
					src={props.img}
				/>
			</div>
		</div>
	);
};

export default CircularPicFrame;
