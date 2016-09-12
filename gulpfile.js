'use strict';

const gulp           = require('gulp');
const gutil          = require('gulp-util');
const del            = require('del');
const concat         = require('gulp-concat');
// const browserSync    = require('browser-sync').create();
const autoprefixer   = require('autoprefixer');
const postcss        = require('gulp-postcss');
const sass           = require('gulp-sass');
const sourcemaps     = require('gulp-sourcemaps');
const source         = require('vinyl-source-stream');
const buffer         = require('vinyl-buffer');
const browserify     = require('browserify');
const uglify         = require('gulp-uglify');
const cssnano        = require('gulp-cssnano');
const gulpif         = require('gulp-if');
const runSequence    = require('run-sequence');
const path           = require('path');
const fs             = require('fs');

const nodeModules = (() => {
  let base = 'node_modules';
  let modulesPath;
  while( true ) {
    let stats;
    const upOne = path.resolve( base );
    console.log(upOne)
    try {
      stats = fs.statSync( upOne );
      if ( stats.isDirectory() ) {
        modulesPath = upOne;
        console.log(modulesPath);
        break;
      }

    } catch( e ) { console.log(e) }
    base = '../' + base;
  }
  return modulesPath;
})();

function bundle(options) {
  options = options || {};
  const bundlerOpts = { entry: true, debug: true };
  let bundler = browserify(
    './islideas/static_src/js/isl-ideas.js', bundlerOpts
    )
    .transform('babelify', { presets: ['es2015'] });

  function rebundle() {
    return bundler.bundle()
      .on('error', function(err) {
        gutil.log(gutil.colors.red(err.message));
        this.emit('end');
      })
      .pipe(source('bundle.js'))
      .pipe(buffer())
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('./islideas/static/js/'));
  }

  if (options.watch) {
    const watchify = require('watchify');
    bundler = watchify(bundler);
    bundler.on('update', () => {
      gutil.log('-> bundling...');
      rebundle();
    });
  }

  return rebundle();
}

gulp.task('browserify', () => {
  return bundle();
});

gulp.task('watchify', () => {
  return bundle({ watch: true });
});

gulp.task('sass', () => {
  return gulp.src('./islideas/static_src/scss/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass(
      {
        includePaths: [
            path.join( nodeModules, '/select2/src/scss/'),
            path.join(path.dirname(require.resolve('foundation-sites')), '../scss')]
      }
    )
    .on('error', sass.logError))
    .pipe(postcss([autoprefixer]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./islideas/static/css/'));
});

gulp.task('extras', () => {
  return gulp.src('./islideas/static_src/**/*.{txt,json,xml,jpeg,jpg,png,gif,svg,ttf,otf,eot,woff, woff2}')
    .pipe(gulp.dest('./islideas/static/'));
});

gulp.task('watch', ['sass', 'extras', 'watchify'], () => {
  // browserSync.init({
  //   proxy: '127.0.0.1:8000'
  // });
  gulp.watch('./islideas/static_src/scss/**/*.scss', ['sass']);
  gulp.watch('./islideas/static_src/**/*.{txt,json,xml,jpeg,jpg,png,gif,svg,ttf,otf,eot,woff, woff2}', ['extras']);
});

gulp.task('banner', ['browserify'], () => {
  return gulp.src(['./public/banner.txt', './islideas/static/js/bundle.js'])
    .pipe(concat('bundle.js'))
    .pipe(gulp.dest('./islideas/static/js/'));
});

gulp.task('minify', () => {
  return gulp.src(['./islideas/static/**/*'],
                  { base: './islideas/static/' })
    // Only target the versioned files with the hash
    // Those files have a - and a 10 character string
    .pipe(gulpif(/\.js$/, uglify()))
    .pipe(gulpif(/\.css$/, cssnano()))
    .pipe(gulp.dest('./islideas/static/'));
});

gulp.task('clean', () => {
  return del('./islideas/static/');
});

gulp.task('build', (done) => {
  runSequence(
    'clean',
    ['browserify', 'sass', 'extras'],
    done
  );
});

gulp.task('build:production', (done) => {
  runSequence(
    'build',
    ['banner', 'minify'],
    done
  );
});

gulp.task('start', (done) => {
  runSequence(
    'build',
    'watch',
    done
  );
});

gulp.task('default', ['build']);
