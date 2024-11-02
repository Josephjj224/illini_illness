import {useState} from "react";
import {Box, FormLabel, Slider, SliderFilledTrack, SliderMark, SliderThumb, SliderTrack} from "@chakra-ui/react";

const InputSlider = ({title, color, value, setValue, ...props}) => {
	return <>
        <FormLabel>{title}: {
            value == 0 ? "not noticable"
            : value == 1 ? "slightly active"
            : value == 2 ? "moderate"
            : value == 3 ? "active"
            : "very active"
        }</FormLabel>
        <Slider
            value={value}
            onChange={setValue}
            min={0}
            max={4}
            mb="14"
            aria-label={title + '-slider'}
            focusThumbOnChange={false}
            {...props}
        >
            <SliderTrack>
                <SliderFilledTrack background={color[500]} />
            </SliderTrack>
            <SliderThumb background={color[500]} />
            <SliderMark value={0} opacity="80%" top="4">Low</SliderMark>
            <SliderMark value={4} opacity="80%" top="4" left="inherit !important" right="0%">High</SliderMark>
        </Slider>
    </>;
};

export default InputSlider;
