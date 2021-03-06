/* -*- c++ -*- */
/*
 * Copyright 2007 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_GRI_GLFSR_H
#define INCLUDED_GRI_GLFSR_H

#include <gr_core_api.h>

/*!
 * \brief Galois Linear Feedback Shift Register using specified polynomial mask
 * \ingroup misc
 *
 * Generates a maximal length pseudo-random sequence of length 2^degree-1
 */

class GR_CORE_API gri_glfsr
{
 private:
  int d_shift_register;
  int d_mask;

 public:

  gri_glfsr(int mask, int seed) { d_shift_register = seed; d_mask = mask; }
  static int glfsr_mask(int degree);

  unsigned char next_bit() {
    unsigned char bit = d_shift_register & 1;
    d_shift_register >>= 1;
    if (bit)
      d_shift_register ^= d_mask;
    return bit;
  }

  int mask() const { return d_mask; }
};

#endif /* INCLUDED_GRI_GLFSR_H */