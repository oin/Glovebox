/*
 GloveBox. An experimental improvised music environment.
 Copyright (C) 2012 Jonathan Aceituno
 http://glovebox.oin.name
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include "webcam_tracker.h"
#include "tracked_object.h"
#include "audio_device.h"
#include "audio_settings.h"
#include "audio_engine.h"
#include "system_audio.h"
#include "ofVec2f.h"
#include "ofVec3f.h"
#include "ofVec4f.h"
#include "ofQuaternion.h"
#include "matrix_decomposition.h"
#include "ofMatrix4x4.h"
#include <string>
#include <vector>

BOOST_PYTHON_MODULE(libglovebox) {
	using namespace boost::python;
	class_<ofVec2f>("Vec2f", init<float,float>())
		.def(self + self)
		.def(self - self)
		.def(self += self)
		.def(self -= self)
		.def(self * self)
		.def(self *= self)
		.def(self / self)
		.def(self /= self)
		.def(self + float())
		.def(float() + self)
		.def(self += float())
		.def(self - float())
		.def(float() - self)
		.def(self -= float())
		.def(self * float())
		.def(float() * self)
		.def(self *= float())
		.def(self / float())
		.def(self /= float())
		.def_readwrite("x", &ofVec2f::x, "The x coordinate of the vector.")
		.def_readwrite("y", &ofVec2f::y, "The y coordinate of the vector.")
		.def("scaled", &ofVec2f::getScaled, "Return this vector scaled by a length.")
		.def("rotated", &ofVec2f::getRotatedRad, "Return this vector rotated by an angle in radians.")
		.def("distance", &ofVec2f::distance, "Return the distance between this vector and another.")
		.def("interpolated", &ofVec2f::interpolated, "Return the linear interpolation between this vector and another, given a coefficient.")
		.def("length", &ofVec2f::length, "Return the length of the vector.")
		.def("angle_with", &ofVec2f::angleRad, "Return the angle in radians between this vector and another.")
		.def("dot", &ofVec2f::dot, "Return the dot product of this vector and another.")
		;
	class_<ofVec3f>("Vec3f", init<float,float,float>())
		.def(self + self)
		.def(self - self)
		.def(self += self)
		.def(self -= self)
		.def(self * self)
		.def(self *= self)
		.def(self / self)
		.def(self /= self)
		.def(self + float())
		.def(float() + self)
		.def(self += float())
		.def(self - float())
		.def(float() - self)
		.def(self -= float())
		.def(self * float())
		.def(float() * self)
		.def(self *= float())
		.def(self / float())
		.def(self /= float())
		.def_readwrite("x", &ofVec3f::x, "The x coordinate of the vector.")
		.def_readwrite("y", &ofVec3f::y, "The y coordinate of the vector.")
		.def_readwrite("z", &ofVec3f::z, "The z coordinate of the vector.")
		.def("scaled", &ofVec3f::getScaled, "Return this vector scaled by a length.")
		.def("distance", &ofVec3f::distance, "Return the distance between this vector and another.")
		.def("interpolated", &ofVec3f::interpolated, "Return the linear interpolation between this vector and another, given a coefficient.")
		.def("length", &ofVec3f::length, "Return the length of the vector.")
		.def("angle_with", &ofVec3f::angleRad, "Return the angle in radians between this vector and another.")
		.def("dot", &ofVec3f::dot, "Return the dot product of this vector and another.")
		;
	class_<ofVec4f>("Vec4f", init<float,float,float,float>())
		.def(self + self)
		.def(self - self)
		.def(self += self)
		.def(self -= self)
		.def(self * self)
		.def(self *= self)
		.def(self / self)
		.def(self /= self)
		.def(self + float())
		.def(float() + self)
		.def(self += float())
		.def(self - float())
		.def(float() - self)
		.def(self -= float())
		.def(self * float())
		.def(float() * self)
		.def(self *= float())
		.def(self / float())
		.def(self /= float())
		.def_readwrite("x", &ofVec4f::x, "The x coordinate of the vector.")
		.def_readwrite("y", &ofVec4f::y, "The y coordinate of the vector.")
		.def_readwrite("z", &ofVec4f::z, "The z coordinate of the vector.")
		.def_readwrite("w", &ofVec4f::w, "The w coordinate of the vector.")
		.def("scaled", &ofVec4f::getScaled, "Return this vector scaled by a length.")
		.def("distance", &ofVec4f::distance, "Return the distance between this vector and another.")
		.def("interpolated", &ofVec4f::interpolated, "Return the linear interpolation between this vector and another, given a coefficient.")
		.def("length", &ofVec4f::length, "Return the length of the vector.")
		.def("dot", &ofVec4f::dot, "Return the dot product of this vector and another.")
		;
	class_<ofQuaternion>("Quaternion", init<float,float,float,float>())
		.def(self + self)
		.def(self - self)
		.def(self += self)
		.def(self -= self)
		.def(self * self)
		.def(self *= self)
		.def(self / self)
		.def(self /= self)
		.def(self * float())
		.def(self *= float())
		.def(self / float())
		.def(self /= float())
		.def_readwrite("coordinates", &ofQuaternion::_v, "The vector coordinates of the quaternion.")
		.def("slerp", &ofQuaternion::slerp, "Make the vector equal to spherical linear interpolation (slerp) between a quaternion and another, given a coefficient.")
		.def("length", &ofQuaternion::length, "Return the length of the vector.")
		.def("conjugate", &ofQuaternion::conj, "Return the conjugate of this quaternion.")
		;
	class_<matrix_decomposition>("MatrixDecomposition")
		.def_readwrite("translation", &matrix_decomposition::translation, "Return the translation vector.")
		.def_readwrite("rotation", &matrix_decomposition::rotation, "Return the rotation quaternion.")
		.def_readwrite("scale", &matrix_decomposition::scale, "Return the scale vector.")
		;
	class_<ofMatrix4x4>("TransformationMatrix")
		.def("get", &ofMatrix4x4::getCoef, "Return the coefficient located at the specified row and column.")
		.def("set", &ofMatrix4x4::setCoef, "Set the coefficient located at the specified row and column.")
		.def("is_valid", &ofMatrix4x4::isValid, "Tell if the matrix is valid, ie. has valid coefficients.")
		.def("decomposed", &ofMatrix4x4::decomposeMatrix, "Return the decomposition of this matrix.")
		.def("recompose", &ofMatrix4x4::recomposeMatrix, "Set the matrix to the specified translation and rotation.")
		.def("load_gl", &ofMatrix4x4::loadGl, "Load the matrix into OpenGL.")
		;
	
	class_<std::vector<float> >("FloatList")
		.def(vector_indexing_suite<std::vector<float> >())
		;
	class_<audio_device>("AudioDevice")
		.def_readonly("name", &audio_device::name, "The system name of the audio device.")
		.def_readonly("nb_input_channels", &audio_device::nb_input_channels, "The number of input channels the audio device can provide.")
		.def_readonly("nb_output_channels", &audio_device::nb_output_channels, "The number of output channels the audio device can provide.")
		// .def_readonly("default_input_latency", &audio_device::default_input_latency)
		// .def_readonly("default_output_latency", &audio_device::default_output_latency)
		.def_readonly("default_sample_rate", &audio_device::default_sample_rate, "The default sample rate of the audio device.")
		;
	class_<std::vector<audio_device> >("AudioDeviceList")
		.def(vector_indexing_suite<std::vector<audio_device> >())
		;
	class_<system_audio>("SystemAudio")
		.def("default_input_device", &system_audio::default_input_device, "Return the default audio input device of the system.")
		.def("default_output_device", &system_audio::default_output_device, "Return the default audio output device of the system.")
		.def_readonly("devices", &system_audio::devices, "A list of the audio devices in the system.")
		;
	class_<audio_settings>("AudioSettings")
		.def_readwrite("input_device", &audio_settings::input_device, "The selected audio input device.")
		.def_readwrite("output_device", &audio_settings::output_device, "The selected audio output device.")
		.def_readwrite("sample_rate", &audio_settings::sample_rate, "The selected audio sample rate.")
		.def_readwrite("buffer_size", &audio_settings::buffer_size, "The selected audio buffer size (must be a multiple of 2).")
		;
	class_<AudioEngine>("AudioEngine")
		.def("open", &AudioEngine::Open, "Open the audio engine. Return false if there's a problem.")
		.def("close", &AudioEngine::Close, "Close the audio engine.")
		.def("start", &AudioEngine::Start, "Start the audio engine.")
		.def("stop", &AudioEngine::Stop, "Stop the audio engine.")
		.def("open_patch", &AudioEngine::OpenPatch, "Open a Puredata patch and returns its identifier in the engine.")
		.def("close_patch", &AudioEngine::ClosePatch, "Close a Puredata patch given its identifier.")
		.def("send_num_to_patch", &AudioEngine::SendToPatchF, "Send a message (string, float) to a patch given its identifier.")
		.def("send_sym_to_patch", &AudioEngine::SendToPatchS, "Send a message (string, string) to a patch given its identifier.")
		.def("redirect_patch_audio_to_master", &AudioEngine::RedirectPatchAudioToMaster, "Redirect the specified patch audio output to the master output.")
		.def("redirect_patch_audio_to_patch", &AudioEngine::RedirectPatchAudioToPatch, "Redirect the specified patch audio output to another patch input.")
		.def("turn_on_patch", &AudioEngine::TurnOnPatch, "Turn on the specified patch (don't forget to do it as it is turned off by default).")
		.def("turn_off_patch", &AudioEngine::TurnOffPatch, "Turn off the specified patch.")
		.def("add_to_patch_search_path", &AudioEngine::AddToPatchSearchPatch, "Add the given path to the patch search path.")
		.def_readonly("input_device", &AudioEngine::input_device, "The open input device.")
		.def_readonly("output_device", &AudioEngine::output_device, "The open output device.")
		;
	
	
	
	
	class_<camera_settings>("CameraSettings")
		.def_readwrite("image_width", &camera_settings::image_width, "The width of the camera image.")
		.def_readwrite("image_height", &camera_settings::image_height, "The height of the camera image.")
		.def_readwrite("desired_framerate", &camera_settings::desired_framerate, "The desired framerate for the camera.")
		.def_readwrite("calibration_file", &camera_settings::calibration_file, "The path to a calibration file (mandatory).")
		;
	
	class_<tracked_object>("TrackedObject")
		.def_readonly("id", &tracked_object::id, "The identifier of the tracked object (corresponds to the fiducial ID).")
		.def_readonly("model_view_matrix", &tracked_object::model_view_matrix, "The model view matrix corresponding to the tracked object.")
		.def_readonly("frame_last_seen", &tracked_object::frame_last_seen, "The last frame number where the tracked object has been seen last.")
		;
	class_<std::map<int, tracked_object> >("TrackedObjectDictionary")
		.def(map_indexing_suite<std::map<int, tracked_object> >())
		;
	
	class_<WebcamTracker>("WebcamTracker")
		.def("open", &WebcamTracker::Open, "Open the tracking system given a camera settings object.")
		.def("show_configuration_window", &WebcamTracker::ShowConfigurationWindow, "Open a camera configuration window.")
		.def("close", &WebcamTracker::Close, "Close the tracking system.")
		.def("start", &WebcamTracker::Start, "Start the tracking system.")
		.def("stop", &WebcamTracker::Stop, "Stop the tracking system.")
		.def("is_open", &WebcamTracker::is_open, "Tell if the tracking system is open.")
		.def("update", &WebcamTracker::Update, "Update the whole tracking process given a frame number.")
		.def("draw_current_frame_gl", &WebcamTracker::DrawCurrentFrame, "Draw the current frame using OpenGL as a textured square in (0;0)->(1;1).")
		.def("project_to_normalized_screen", &WebcamTracker::ProjectToNormalizedScreen, "Return the 2D normalized coordinates of a given transformation projected on the screen.")
		.def_readonly("objects", &WebcamTracker::objects, "The tracked objects.")
		.def_readonly("projection_matrix", &WebcamTracker::projection_matrix, "The camera projection matrix.")
		;
}