<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/hello', 'PagesController@hello');
Route::get('/', 'DashboardController@index');
Route::get('/register', 'PagesController@register');
Route::get('/login', 'PagesController@login');


Route::resource('articles', 'ArticlesController');

Auth::routes();

Route::get('/dashboard', 'DashboardController@index')->name('dashboard');
