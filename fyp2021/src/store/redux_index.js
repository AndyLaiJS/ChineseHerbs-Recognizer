import { createSlice, configureStore } from "@reduxjs/toolkit";

const initialState = {
	Label: "",
	Desc: "",
};

const recognizerSlice = createSlice({
	name: "Recognizer",
	initialState,
	reducers: {
		updateStore(state, action) {
			state.Label = action.payload.label;
			state.Desc = action.payload.desc;
		},
	},
});

const store = configureStore({ reducer: recognizerSlice.reducer });

export const recognizerActions = recognizerSlice.actions;
export default store;
