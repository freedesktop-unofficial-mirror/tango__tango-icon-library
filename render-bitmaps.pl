#!/usr/bin/perl -w
# -*- Mode: perl; indent-tabs-mode: nil; c-basic-offset: 4  -*-
#############################################################################
## Copyright (C) 2008 Rodney Dawes
##
## Authors: Rodney Dawes <dobey@gnome.org>
##

use strict;
use XML::Simple;
use Getopt::Long;

my $inkscape = "inkscape";
my $sizeonly;
my $outdir;
my $dirall;

############################################################################
my @default_getopt_config = ("permute", "pass_through", "bundling",
			     "no_auto_abbrev", "no_ignore_case");

Getopt::Long::Configure (@default_getopt_config);
GetOptions ("size|s=s" => \$sizeonly,
            "inkscape|i=s" => \$inkscape,
            "output-dir|o=s" => \$outdir,
            "directory|d=s" => \$dirall);

############################################################################

use Data::Dumper;

sub render_icons {
    my $filename = shift;

    my $mapping = XML::Simple::XMLin ($filename,
				      keyattr => [ qw() ],
				      forcearray => [ qw(g rect text) ]);

    foreach my $icon (@{$mapping->{g}}) {
	my $name;
	my $context;

	foreach my $plate (@{$icon->{g}}) {
	    if (defined $plate->{'inkscape:label'} &&
		$plate->{'inkscape:label'} =~ m/plate(.*)/) {

		foreach my $text (@{$plate->{text}}) {
		    if (defined $text->{'inkscape:label'} &&
			$text->{'inkscape:label'} eq "icon-name") {
			$name = $text->{tspan}->{content};
		    } elsif (defined $text->{'inkscape:label'} &&
			$text->{'inkscape:label'} eq "context") {
			$context = $text->{tspan}->{content};
		    }
		}
		foreach my $box (@{$plate->{rect}}) {
		    if (defined $box->{'inkscape:label'}) {
			my $size = $box->{'inkscape:label'};
			my $dir = "$size/$context";

                        next if (defined $sizeonly && $size ne $sizeonly);

			if (! -d $dir) {
			    system ("mkdir -p $dir");
			}
			my $cmd = "$inkscape -i $box->{id} -e $dir/$name.png $filename > /dev/null";
                        print "Rendering $dir/$name.png...\n";
			system ($cmd);
		    }
		}
	    }
	}
    }
}

sub usage {
    print "Usage: render-bitmaps.pl [OPTIONS] <SVGFILE>

  -d, --directory=<dir>     Render all SVGs in <dir>
  -i, --inkscape=<path>     Path to inkscape binary to use
  -o, --output=<dirname>    Directory to output PNGs to
  -s, --size=<size>         Size to render from <SVGFILE>

";

    exit 1;
}

if (defined $ARGV[0]) {
    render_icons ($ARGV[0]);
} elsif (defined $dirall) {
    opendir (DIR, $dirall) || die ("ERROR: Failed to open directory: $dirall");
    my @filelist = readdir (DIR);
    closedir (DIR);

    foreach my $file (@filelist) {
        next if ($file eq "." || $file eq "..");
        render_icons ("$dirall/$file") if ($file =~ m/^(.*).svg[z]?$/);
    }
} else {
    usage ();
}
