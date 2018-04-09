import scala.io.Source
import scala.util.Try

object Wrapper {
  private def mkUrl(method_name: String, v: String, parameters: Seq[String]): String = {
    s"https://api.vk.com/method/$method_name.xml?${parameters.mkString("&")}&v=$v"
  }

  def mkQuery(method_name: String, v: String, parameters: Seq[String]): Try[String] = {
    Try[String](Source.fromURL(mkUrl(method_name, v, parameters), "utf-8").mkString)
  }
}
