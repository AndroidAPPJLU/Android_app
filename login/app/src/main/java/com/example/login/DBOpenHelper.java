package com.example.login;

import android.annotation.SuppressLint;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;

public class DBOpenHelper extends SQLiteOpenHelper {
    private SQLiteDatabase db;

    static String DATABASE_NAME="User";
    static String CREATE_SQL="CREATE TABLE IF NOT EXISTS User(id integer primary key autoincrement, name text,password text)";//建表
    static String DROP_SQL="DROP TABLE IF EXISTS User";

    public DBOpenHelper (Context context){
        super(context,DATABASE_NAME,null,1);
        db=getReadableDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(CREATE_SQL);

    }

    @Override
    public void onUpgrade(SQLiteDatabase sqLiteDatabase, int i, int i1) {
        db.execSQL(DROP_SQL);
        onCreate(db);

    }
    //增删改查
    static private String INSERT_SQL="INSERT INTO User (name,password) VALUES(?,?)";
    static private String DELETE_SQL="DELETE FROM User WHERE name= AND password =";

    public void add(String name,String password){
        db.execSQL(INSERT_SQL,new Object[]{name,password});
    }
    public void delete(String name,String password){
        db.execSQL(DELETE_SQL+name+password);
    }
    public void update(String name,String password){
        db.execSQL("UPDATE User SET password = ?",new Object[]{password});
    }

    public ArrayList<User> getAllDate(){

        ArrayList<User> list=new ArrayList<User>();
        Cursor cursor=db.query("User",null,null,null,null,null,"name DESC");
        while (cursor.moveToNext()){
            @SuppressLint("Range") String name=cursor.getString(cursor.getColumnIndex("name"));
            @SuppressLint("Range") String password = cursor.getString(cursor.getColumnIndex("password"));
            list.add(new User(name,password));

        }
        return list;
    }
}
