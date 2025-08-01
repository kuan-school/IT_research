/* Bring in the gd library functions */
#include "gd.h"

/* Bring in standard I/O and string manipulation functions */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
	FILE *in;
	FILE *out;
	/* Declare our image pointer */
	gdImagePtr im = 0;
	int i;
       /* We'll clear 'no' once we know the user has made a
		reasonable request. */
	int no = 1;
	/* We'll set 'write' once we know the user's request
		requires that the image be written back to disk. */
	int write = 0;
	/* C programs always get at least one argument; we want at
		least one more (the image), more in practice. */
	if (argc < 2) {
		no = 1;	
		goto usage;
	}
	/* The last argument should be the image. Open the file. */
	in = fopen(argv[argc-1], "rb");	
	if (!in) {
		fprintf(stderr,
			"Error: can't open file %s.\n", argv[argc-1]);
	}
	/* Now load the image. */	
	im = gdImageCreateFromGif(in);
	fclose(in);
	/* If the load failed, it must not be a GIF file. */
	if (!im) {
		fprintf(stderr,
			"Error: %s is not a valid gif file.\n", argv[1]);
		exit(1);	
	}
	/* Consider each argument in turn. */
	for (i=1; (i < (argc-1)); i++) {
		/* -i turns on and off interlacing. */
		if (!strcmp(argv[i], "-i")) {
			if (i == (argc-2)) {
				fprintf(stderr, 
				"Error: -i specified without y or n.\n");
				no = 1;
				goto usage;
			}
			if (!strcmp(argv[i+1], "y")) {
				/* Set interlace. */
				gdImageInterlace(im, 1);
			} else if (!strcmp(argv[i+1], "n")) {
				/* Clear interlace. */
				gdImageInterlace(im, 0);
			} else {
				fprintf(stderr,
				"Error: -i specified without y or n.\n");
				no = 1;
				goto usage;
			}
			i++;
			no = 0;
			write = 1;
		} else if (!strcmp(argv[i], "-t")) {
			/* Set transparent index (or none). */
			int index;
			if (i == (argc-2)) {
				fprintf(stderr,
		"Error: -t specified without a color table index.\n");
				no = 1;
				goto usage;
			}
			if (!strcmp(argv[i+1], "none")) {
				/* -1 means not transparent. */
				gdImageColorTransparent(im, -1);
			} else {
				/* OK, get an integer and set the index. */
				index = atoi(argv[i+1]);
				gdImageColorTransparent(im, index);
			}
			i++;
			write = 1;
			no = 0;
		} else if (!strcmp(argv[i], "-l")) {
			/* List the colors in the color table. */
			int j;
			/* Tabs used below. */
			printf("Index	Red	Green	Blue\n");
			for (j=0; (j < gdImageColorsTotal(im)); j++) {
				/* Use access macros to learn colors. */
				printf("%d	%d	%d	%d\n",
					j, 
					gdImageRed(im, j),
					gdImageGreen(im, j),
					gdImageBlue(im, j));
			}
			no = 0;
		} else if (!strcmp(argv[i], "-d")) {
			/* Output dimensions, etc. */
			int t;
			printf("Width: %d Height: %d Colors: %d\n",
				gdImageSX(im), gdImageSY(im),
				gdImageColorsTotal(im));
			t = gdImageGetTransparent(im);
			if (t != (-1)) {
				printf("Transparent index: %d\n", t);
			} else {
				/* -1 means the image is not transparent. */
				printf("Transparent index: none\n");
			}
			if (gdImageGetInterlaced(im)) {
				printf("Interlaced: yes\n");	
			} else {
				printf("Interlaced: no\n");	
			}
			no = 0;
		} else {
			fprintf(stderr, "Unknown argument: %s\n", argv[i]);
			break;	
		}
	}
usage:
	if (no) {
		/* If the command failed, output an explanation. */
		fprintf(stderr, 
	"Usage: webgif [-i y|n ] [-l] [-t index|off ] [-d] gifname.gif\n");
		fprintf(stderr, 
	"Where -i controls interlace (specify y or n for yes or no),\n");
		fprintf(stderr, 
	"-l outputs a table of color indexes, -t sets the specified\n");
		fprintf(stderr, 
	"color index (0-255 or none) to be the transparent color, and\n");
		fprintf(stderr,
	"-d reports the dimensions and other characteristics of the image.\n");
		fprintf(stderr, 
	"Note: you may wish to pipe to \"more\" when using the -l option.\n");
	} 
	if (write) {
		/* Open a temporary file. */
		out = fopen("temp.tmp", "wb");
		if (!out) {
			fprintf(stderr,
				"Unable to write to temp.tmp -- exiting\n");
			exit(1);
		}
		/* Write the new gif. */
		gdImageGif(im, out);
		fclose(out);
		/* Erase the old gif. */
		unlink(argv[argc-1]);
		/* Rename the new to the old. */
		rename("temp.tmp", argv[argc-1]);
	}
	/* Delete the image from memory. */
	if (im) {
		gdImageDestroy(im);
	}
	/* All's well that ends well. */
	return 0;
}

