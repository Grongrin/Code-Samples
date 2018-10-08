<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PagesController extends Controller
{
        /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth', ['except' => ['hello', 'index']]);
    }

    public function hello(){
        return view('pages.hello');
    }

    public function index(){
        return view('pages.index');
    }

}
