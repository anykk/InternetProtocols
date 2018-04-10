import scala.util.Try
import scala.xml._


trait ApiWrapper {
  private def mkUrl(method_name: String, v: String, parameters: Seq[String]): String = {
    s"https://api.vk.com/method/$method_name.xml?${parameters.mkString("&")}&v=$v"
  }

  protected def mkQuery(method_name: String, v: String, parameters: Seq[String]): Try[Elem] = {
    Try[Elem] {
      XML.load(mkUrl(method_name, v, parameters))
    }
  }
}
