@extends('layouts.app')

@section('content')
        
    <h1>{{$article->title}}</h1>
    <small>Author: {{$article->user->name}}</small>

    <br/><br/>
    <p>{!!$article->body!!}</p>

    
    <hr>
    <small>(Written on {{$article->created_at}}
        @if($article->created_at != $article->updated_at)
            | Last edited on {{$article->updated_at}}
        @endif
    )</small><br/>

    @if(!Auth::guest() && auth()->user()->id == $article->user_id)

        <a href="/articles/{{$article->id}}/edit" class='btn btn-primary'>Edit</a>

        {!!Form::open(['action' => ['ArticlesController@destroy', $article->id], 'method' => 'POST', 'class' => 'float-right'])!!}
            {{Form::hidden('_method', 'DELETE')}}
            {{Form::submit('Delete', ['class'=>'btn btn-danger'])}}
        {!!Form::close()!!}
    @endif

@endsection
