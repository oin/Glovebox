#ifndef MATRIX_DECOMPOSITION_H_UH702UJ8
#define MATRIX_DECOMPOSITION_H_UH702UJ8

#include "ofVec3f.h"
#include "ofQuaternion.h"

struct matrix_decomposition {
	ofVec3f translation;
	ofQuaternion rotation;
	ofVec3f scale;
	ofQuaternion so;
};

#endif /* end of include guard: MATRIX_DECOMPOSITION_H_UH702UJ8 */
