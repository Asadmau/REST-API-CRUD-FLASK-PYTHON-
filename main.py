import pymysql
from app import app
from koneksi import dbsql
from flask import jsonify
from flask import flash, request


@app.route('/add', methods=['POST'])
def add_produk():
    try:
        _json = request.json
        # _id = _json['produk_id']
        _nameproduk = _json['nama_produk']
        _stok = _json['stok']
        _harga = _json['harga']
        _keterangan = _json['keterangan']
        _status = _json['status']
        if _nameproduk and _stok and _harga and _keterangan and _status and request.method == 'POST':
            query = "insert into produk( nama_produk, stok, harga, keterangan, status) values( %s, %s, %s, %s, %s)"
            binData = (_nameproduk, _stok, _harga, _keterangan, _status)
            conn = dbsql.connect()
            cursor = conn.cursor()
            cursor.execute(query, binData)
            conn.commit()
            resp = jsonify('Employee added succesfull', binData)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
# menampilkan semua data dari database


@app.route('/produk')
def tampil():
    try:
        conn = dbsql.connect()
        cur = conn.cursor()
        cur.execute('select * from produk')
        produkrow = cur.fetchall()
        res = jsonify(produkrow)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
# untuk menampilkan satu data


@app.route('/produk/<int:id>')
def tampilid(id):
    try:
        conn = dbsql.connect()
        cur = conn.cursor()
        cur.execute('select * from produk where produk_id=%s', id)
        produkrow = cur.fetchone()
        res = jsonify(produkrow)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
# edit data


@app.route('/edit', methods=['PUT'])
def edit():
    try:
        _json = request.json
        _id = _json['produk_id']
        _nameproduk = _json['nama_produk']
        _stok = _json['stok']
        _harga = _json['harga']
        _keterangan = _json['keterangan']
        _status = _json['status']
        if _nameproduk and _stok and _harga and _keterangan and _status and _id and request.method == 'PUT':
            query = "update produk set nama_produk=%s, stok=%s, harga=%s, keterangan=%s, status=%s where produk_id=%s"
            binData = (_nameproduk, _stok, _harga, _keterangan, _status, _id)
            conn = dbsql.connect()
            cursor = conn.cursor()
            cursor.execute(query, binData)
            conn.commit()
            resp = jsonify('Edit succesfull', binData)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
# delete data


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        conn = dbsql.connect()
        cur = conn.cursor()
        cur.execute('delete from produk where produk_id=%s', (id,))
        # produkrow = cur.fetchone()
        conn.commit()
        res = jsonify('berhasil di hapus')
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

# mengatur error


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404
    return res


if __name__ == "__main__":
    app.run(debug=True, port=2000)
