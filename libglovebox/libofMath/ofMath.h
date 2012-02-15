#ifndef OFMATH_H_5HX3VZ44
#define OFMATH_H_5HX3VZ44

#include "ofConstants.h"

int next_power_of_two(int);
float		ofNormalize(float value, float min, float max);
float		ofMap(float value, float inputMin, float inputMax, float outputMin, float outputMax, bool clamp = false);
float		ofClamp(float value, float min, float max);
float		ofLerp(float start, float stop, float amt);
float		ofDist(float x1, float y1, float x2, float y2);
float		ofDistSquared(float x1, float y1, float x2, float y2);
int			ofSign(float n);
bool		ofInRange(float t, float min, float max);

float		ofRadToDeg(float radians);
float		ofDegToRad(float degrees);
float 		ofLerpDegrees(float currentAngle, float targetAngle, float pct);
float 		ofLerpRadians(float currentAngle, float targetAngle, float pct);
float 		ofAngleDifferenceDegrees(float currentAngle, float targetAngle);
float 		ofAngleDifferenceRadians(float currentAngle, float targetAngle);
float 		ofAngleSumRadians(float currentAngle, float targetAngle);
float		ofWrapRadians(float angle, float from = -PI, float to=+PI);
float		ofWrapDegrees(float angle, float from = -180, float to=+180);

#endif /* end of include guard: OFMATH_H_5HX3VZ44 */
