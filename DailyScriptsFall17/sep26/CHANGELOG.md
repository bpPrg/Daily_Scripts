
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

* [Jesisim v1.0](#jesisim-v10)
* [Jedisim v2.0](#jedisim-v20)
* [Jedisim  v3.0](#jedisim-v30)
	* [1: Interpolate user given sed](#interpolate-user-given-sed)
	* [2: Create bulge and disk weights for given z](#create-bulge-and-disk-weights-for-given-z)
	* [3: Create scaled bulge and scaled disk fitsfiles](#create-scaled-bulge-and-scaled-disk-fitsfiles)
	* [4: Get fraction of flux of all scaled_bulges to to all scaled disks](#get-fraction-of-flux-of-all-scaled_bulges-to-to-all-scaled-disks)
	* [5: Create PSF for bulge, disk, and mono](#create-psf-for-bulge-disk-and-mono)
	* [6: Get convolved images of bulge, disk, mono and chromatic images](#get-convolved-images-of-bulge-disk-mono-and-chromatic-images)

<!-- /code_chunk_output -->



# Jesisim v1.0
It takes a single galaxy input image, convolves with a given psf and
creates a single output file.

# Jedisim v2.0
This program **Jedisim** takes in bulge and disk components HST WFT ACS f814w filter images
(f814w_gal*.fits) which has pixscale 0.06 and and creates a realistic set of
output images with pixscale 0.2 for LSST r band filter.

The bulge and disk component are created using galfit program.


```python
def run_7programs_loop():
    for i in range(0, 21):
        run_process("jedicolor", ['./executables/jedicolor',
        run_process("jeditransform"]
        run_process("jedidistort",
        run_process("jedipaste", ['./executables/jedipaste',
        run_process("jediconvolve",
        run_process("jedipaste", ['./executables/jedipaste',
        run_process("jedirescale",


def average21_and_add_noise():
    config = update_config()
    run_process("jediaverage", ['./executables/jediaverage']
    run_process("jedinoise", ['./executables/jedinoise']
    run_process("jedinoise", ['./executables/jedinoise']
```

# Jedisim  v3.0
The new file structure is given below:

  - a1_interpolate_sed.py
  - a2_bd_weights.py
  - a3_gen_scaled_bd.py
  - a4_scaled_bd_flux_rat.py
  - a5_psf_bdmono.py
  - a6_jedisim_ofiles.py
  - a7_jedisim_odirs.py
  - a8_jedisim_3cats.py
  - a9_jedisimulate.py
  - a10_jedisimulate90.py
  - jedisim.py
  - run_jedisim.py
  - util.py

<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
<!-- # Subheader:                                         -->
<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
## 1: Interpolate user given sed
The script `a1_interpolate_sed.py` takes in the user given sed file and creates the 1 Angstrom separated interpolated sed files for given redshift.

For example:
Inputs are
`sed/ssp_pf.cat`
`sed/exp9_pf.cat`
and outputs are         `sed/ssp_pf_interpolated_z1.5.cat`
`sed/exp9_pf_interpolated_z1.5.cat`

<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
<!-- # Subheader:                                         -->
<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
<!-- #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* -->
## 2: Create bulge and disk weights for given z
The script `a2_bd_weights.py` takes in these interpolated sed files and creates a text file
containing the weights for bulge and disk for a given redshift.
The output is `physics_settings/bd_weights_z1.5.txt`
The wavelength for LSST r band and HST ACS f814 filter for z = 1.5 and 6 Gyr old
star is:
\[
 \begin{eqnarray}
 \lambda_0 = \frac{5520}{1 + z} = 2208.0 \\
 \lambda_{20} = \frac{6910}{1+z} = 2764 \\
 \lambda_{hst0} = \frac{8333- 2511/2}{1+z_c} = 5897.9 \\
 \lambda_{hst20} = \frac{8333 + 2511/2}{1+z_c} = 7990.4
 \end{eqnarray}
\]


The formula to calculate bulge and disk weight for the first narrowband is:
\[
 \begin{eqnarray}
b[0] = \frac{\int_{\lambda0}^{\lambda1} f_b(\lambda)d\lambda}{\int_{\lambda0}^{\lambda_{20}} f_b(\lambda)d\lambda} \\
d[0] = \frac{\int_{\lambda0}^{\lambda1} f_d(\lambda)d\lambda}{\int_{\lambda0}^{\lambda_{20}} f_d(\lambda)d\lambda}
\end{eqnarray}
\]

## 3: Create scaled bulge and scaled disk fitsfiles
The script `a3_gen_scaled_bd.py ` geneates scaled bulge fitsfiles from the bulge and disk fitsfiles.
The bulge and disk components of given base galaxy were created using the program `galfit`.

Scaled bulge is given by this formula:
\[
 \begin{eqnarray}
scaled\_bulge.fits =  \frac{b0 + b1 + ... + b20}{21} * bulge.fits \\
scaled\_disk.fits =  \frac{d0 + d1 + ... + d20}{21} * disk.fits
\end{eqnarray}
\]

In the actual simulation the names of the  files are:    
`simdatabase/scaled_bulge_f8/f814w_scaled_bulge0.fits`  
`simdatabase/scaled_disk_f8/f814w_scaled_disk0.fits`

Upto bulge_200.fits and disk_200.fits.


## 4: Get fraction of flux of all scaled_bulges to to all scaled disks
We use the script `scaled_bd_flux_rat.py` to ratio of the total flux of all
scaled bulge files (201 files) to the total flux of all the scaled disk files.

We define a quantity $fr$ as
\[
 \begin{eqnarray}
f_r = \frac{\sum  \frac{f_{sb}}{f_{sd}}}{n_g}
\end{eqnarray}
\]

Here, $f_{sb}$ is the flux of the given scaled bulge,
$f_{sd}$ is the flux of the given scaled disk and $n_g$ is number of galaxies.
For example n_g = 201.

Then, we calculate disk part and bulge part of f_r as:
\[
 \begin{eqnarray}
f_{rd} = \frac{1}{1 + f_r} \\
f_{rb} = \frac{f_r}{1 + f_r} = 1 - f_{sd}
\end{eqnarray}
\]

## 5: Create PSF for bulge, disk, and mono
We use the script `psf_bdmono.py`  to create the PSF for the scaled bulge, scaled disk and monochromatic images of the galaxy.
I.e.

\[
 \begin{eqnarray}
p_b = \frac{b0*p0 + b1*p1 + ... + b20*p20}{b0 + b1 + ... + b20} \\
p_d = \frac{d0*p0 + d1*p1 + ... + d20*p20}{d0 + d1 + ... + d20} \\
p_m = f_{rd} \ p_d + f_{rb} \ p_b
\end{eqnarray}
\]
<!-- #*-*-*-*--*-*-*-*-*-*-*-* -->

## 6: Get convolved images of bulge, disk, mono and chromatic images
For the unrotated and 90 degree rotated cases we get the convolved images of the
bulge, disk, monochromatic and chromatic images for each of the base galaxies.
We also save the catalog.txt, dislist.txt and PSF files.

If we run the `jedisim` program once we get following outputs:

 - convolved_scaled_bulge.fits and convolved_scaled_bulge90.fits.
 - convolved_scaled_bulge.fits and convolved_scaled_bulge90.fits.
 - lsst.fits and lsst90.fits
 - lsst_mono.fits and lsst_mono90.fits
 - catalog.txt, dislist.txt
 - psfb.fits, psfd.fits, psfm.fits

Here, we get following convolved files:
\[
 \begin{eqnarray}
g_{csb} = g_{sb} \otimes p_b \\
g_{csd} = g_{sd} \otimes p_d \\
g_{chro} = g_{csb} + g_{csd}  \\
g_{mono} = (g_{sb} + g_{sd}) \otimes p_m  \\
\end{eqnarray}
\]
