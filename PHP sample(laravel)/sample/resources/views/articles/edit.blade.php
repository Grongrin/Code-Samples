@extends('layouts.app')

@section('content')

    <h1>Edit article</h1>
    {!! Form::open(['action' => ['ArticlesController@update', $article->id], 'method' => 'POST']) !!}
        <div class="form-group">
            {{Form::label('title', 'Title')}}
            {{Form::text('title', $article->title, ['class' => 'form-control', 'placeholder' => 'Title'])}}
        </div> 
        <div class="form-group">
            {{Form::label('body', 'Body')}}
            {{Form::textarea('body', $article->body, ['id' => 'article-ckeditor', 'class' => 'form-control', 'placeholder' => 'Body'])}}
        </div> 
        {{Form::hidden('_method', 'PUT')}}
        {{Form::submit('Update', ['class'=>'btn btn-primary'])}}
    {!! Form::close() !!}

@endsection