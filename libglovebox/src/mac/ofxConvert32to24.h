#ifndef OFXCONVERT32TO24_H_GMSYVMVE
#define OFXCONVERT32TO24_H_GMSYVMVE

// Borrowed heavily from ofQtUtils.cpp
typedef struct {
	unsigned char r;
	unsigned char g;
	unsigned char b;
} pix24;
void Convert32To24Pixels(unsigned char* gWorldPixels, unsigned char* rgbPixels, int w, int h) {
	int* rgbaPtr = reinterpret_cast<int*>(gWorldPixels);
	pix24* rgbPtr = reinterpret_cast<pix24*>(rgbPixels);
	unsigned char* rgbaStart;

	//	putting in the boolean, so we can work on
	//	0,0 in top right...
	//	bool bFlipVertically 	= true;

	bool bFlipVertically 	= false;

	// -------------------------------------------
	// we flip vertically because the 0,0 position in OF
	// is the bottom left (not top left, like processing)
	// since the 0,0 of a picture is top left
	// if we upload and drawf the data as is
	// it will be upside-down....
	// -------------------------------------------

	if (!bFlipVertically){
		//----- argb->rgb
		for (int i = 0; i < h; i++){
			rgbPtr = rgbPtr + ((i) * w);
			for (int j = 0; j < w; j++){
				rgbaStart = (unsigned char *)rgbaPtr;
				memcpy (rgbPtr, rgbaStart+1, sizeof(pix24));
				rgbPtr++;
				rgbaPtr++;
			}
		}
	} else {
		for (int i = 0; i < h; i++){
			rgbPtr = rgbPtr + ((h-i-1) * w);
			for (int j = 0; j < w; j++){
				rgbaStart = (unsigned char *)rgbaPtr;
				memcpy (rgbPtr, rgbaStart+1, sizeof(pix24));
				rgbPtr++;
				rgbaPtr++;
			}
		}
	}
}

#endif /* end of include guard: OFXCONVERT32TO24_H_GMSYVMVE */
