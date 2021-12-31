const gulp = require('gulp');
const gulpRename = require('gulp-rename');
const gulpSass = require('gulp-sass')(require('sass'));

gulp.task('sass', function () {
    return gulp.src('./scss/default.scss')
        .pipe(gulpSass({outputStyle: 'compressed'}).on('error', gulpSass.logError))
        .pipe(gulpRename('default.min.css'))
        .pipe(gulp.dest('./../static/css'));
});

gulp.task('default', function () {
    return gulp.watch(
        ['./scss/**/*.scss'],
        gulp.parallel('sass')
    );
});