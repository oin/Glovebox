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

#ifndef GL_TEXTURE_H_MDM5BEA8
#define GL_TEXTURE_H_MDM5BEA8

#include <OpenGL/gl.h>

struct GlTexture {
	GlTexture(unsigned int w, unsigned int h);
	~GlTexture();
	void Load(unsigned char*);
	void Draw(float w, float h);
	int width, height;
	unsigned char* data;
private:
	GLuint texid_;
};

#endif /* end of include guard: GL_TEXTURE_H_MDM5BEA8 */
